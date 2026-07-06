#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR
TMP_DIR = REPO_ROOT / "tmp"
RELEASES_JSON_URL = "https://downloads.php.net/~windows/releases/releases.json"


def print_help():
	parser.print_help()


def get_releases_json():
	cache_file = TMP_DIR / "releases.json"
	TMP_DIR.mkdir(parents=True, exist_ok=True)

	if cache_file.exists():
		cache_age = time.time() - cache_file.stat().st_mtime
		if cache_age <= 604800:
			with open(cache_file) as f:
				return f.read()

	print("Fetching releases.json...")
	try:
		with urllib.request.urlopen(RELEASES_JSON_URL) as response:
			data = response.read().decode("utf-8")
		with open(cache_file, "w") as f:
			f.write(data)
		return data
	except Exception as e:
		print(f"Error: failed to fetch {RELEASES_JSON_URL}: {e}", file=sys.stderr)
		sys.exit(1)


def require_cmd(cmd):
	# Only check for commands that aren't built into Python
	external_cmds = {"curl"}
	if cmd in external_cmds and shutil.which(cmd) is None:
		print(f"Error: required command '{cmd}' not found.", file=sys.stderr)
		sys.exit(1)


def list_available():
	require_cmd("curl")
	require_cmd("unzip")

	data = get_releases_json()

	print("Available PHP NTS versions:")
	versions = sorted(set(re.findall(r'"([0-9]+\.[0-9]+\.[0-9]+)"', data)), key=lambda v: tuple(map(int, v.split("."))))

	for ver in versions[-50:]:
		if re.search(rf"php-{re.escape(ver)}-nts-Win32", data):
			print(f"  {ver}")


def resolve_version(requested, data):
	if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", requested):
		if re.search(rf"php-{re.escape(requested)}-nts-Win32", data):
			return requested
		print(f"Error: PHP version '{requested}' not found.", file=sys.stderr)
		sys.exit(2)

	if re.fullmatch(r"[0-9]+\.[0-9]+", requested):
		matches = re.findall(rf"php-({re.escape(requested)}\.[0-9]+)-nts-Win32", data)
		if matches:
			matches.sort(key=lambda v: tuple(map(int, v.split("."))))
			return matches[-1]
		print(f"Error: no releases match version '{requested}'.", file=sys.stderr)
		sys.exit(2)

	print("Error: invalid version format. Use 8.5 or 8.5.4.", file=sys.stderr)
	sys.exit(2)


def detect_arch():
	import platform
	system_arch = platform.machine().lower()

	if system_arch in ("x86_64", "amd64"):
		return "x64"
	if system_arch in ("aarch64", "arm64"):
		return "arm64"
	if system_arch in ("i386", "i686", "x86"):
		return "x86"
	return "x64"


def find_download_url(version, arch="auto", data=None):
	require_cmd("curl")
	require_cmd("grep")
	require_cmd("sed")

	if data is None:
		data = get_releases_json()

	if arch == "auto":
		arch = detect_arch()

	archs_to_try = []
	if arch == "x64":
		archs_to_try = ["x64", "arm64", "x86"]
	elif arch == "arm64":
		archs_to_try = ["arm64", "x64", "x86"]
	elif arch == "x86":
		archs_to_try = ["x86", "x64", "arm64"]
	else:
		archs_to_try = ["x64", "arm64", "x86"]

	for try_arch in archs_to_try:
		pattern = rf"php-{re.escape(version)}-nts-Win32-[^\"]*-{re.escape(try_arch)}\.zip"
		match = re.search(pattern, data)
		if match:
			return match.group(0)

	print(f"Error: no NTS package found for PHP {version}.", file=sys.stderr)
	sys.exit(3)


def download_and_extract(filename, target):
	url = f"https://downloads.php.net/~windows/releases/{filename}"

	require_cmd("curl")

	TMP_DIR.mkdir(parents=True, exist_ok=True)
	zip_file = TMP_DIR / filename

	if not zip_file.exists():
		print(f"Downloading {filename}...")
		try:
			urllib.request.urlretrieve(url, zip_file)
		except Exception as e:
			print(f"Error: failed to download: {e}", file=sys.stderr)
			sys.exit(1)
	else:
		print(f"Using cached {filename}...")

	with tempfile.TemporaryDirectory() as tmpdir:
		print("Extracting...")
		try:
			with zipfile.ZipFile(zip_file, "r") as zf:
				zf.extractall(tmpdir)
		except Exception as e:
			print(f"Error: failed to extract archive: {e}", file=sys.stderr)
			sys.exit(1)

		entries = [p for p in Path(tmpdir).iterdir() if not p.name.startswith(".")]
		if len(entries) == 1 and entries[0].is_dir():
			source_dir = entries[0]
		else:
			source_dir = Path(tmpdir)

		target.mkdir(parents=True, exist_ok=True)
		for item in source_dir.iterdir():
			shutil.move(str(item), str(target / item.name))

		if not (target / "php.ini").exists() and (target / "php.ini-development").exists():
			shutil.copy(target / "php.ini-development", target / "php.ini")
			print("Created php.ini from php.ini-development")

		print(f"Installed into {target}")


def install_php(args):
	version = args.version
	folder = args.folder
	arch = args.arch
	force = args.force

	data = get_releases_json()
	version = resolve_version(version, data)

	if not folder:
		folder = f"php{version.split('.')[0]}{version.split('.')[1]}"

	target = REPO_ROOT / folder

	if target.exists() and not force:
		print(f"Error: {target} already exists. Use --force to overwrite.", file=sys.stderr)
		sys.exit(1)

	filename = find_download_url(version, arch, data)
	download_and_extract(filename, target)

	print(f"✓ PHP {version} installed to {folder}")


def list_installed_versions():
	found = False
	print(f"{'FOLDER':<20} {'VERSION'}")
	print(f"{'------':<20} {'-------'}")

	for dir_path in sorted(REPO_ROOT.glob("php*")):
		if not dir_path.is_dir():
			continue
		found = True
		folder = dir_path.name
		version = "unknown"

		php_exe = dir_path / "php.exe"
		php_bin = dir_path / "php"
		if php_exe.exists():
			try:
				result = subprocess.run([str(php_exe), "-v"], capture_output=True, text=True, timeout=5)
				version = result.stdout.splitlines()[0].split()[1] if result.stdout else "unknown"
			except Exception:
				pass
		elif php_bin.exists():
			try:
				result = subprocess.run([str(php_bin), "-v"], capture_output=True, text=True, timeout=5)
				version = result.stdout.splitlines()[0].split()[1] if result.stdout else "unknown"
			except Exception:
				pass

		print(f"{folder:<20} {version}")

	if not found:
		print("No installed php* folders found.")


def main():
	global parser
	parser = argparse.ArgumentParser(
		description="PHP Manager for Windows - Download and manage PHP NTS binaries",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  man-php.py list-available
  man-php.py list-installed
  man-php.py install 8.5
  man-php.py install 8.5.4 php85
  man-php.py install --arch x86 8.4 php84custom
  man-php.py install --force 8.5
		"""
	)
	parser.add_argument("command", choices=["list-available", "list-installed", "install", "help"], nargs="?")
	parser.add_argument("version", nargs="?")
	parser.add_argument("folder", nargs="?")
	parser.add_argument("--arch", choices=["x64", "x86", "arm64"], default="auto", help="Force architecture (default: auto)")
	parser.add_argument("--force", action="store_true", help="Overwrite target folder if it exists")

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)

	args = parser.parse_args()

	if args.command in (None, "help"):
		parser.print_help()
		sys.exit(0)

	if args.command == "list-available":
		list_available()
	elif args.command == "list-installed":
		list_installed_versions()
	elif args.command == "install":
		if not args.version:
			print("Error: install requires <version>", file=sys.stderr)
			parser.print_help()
			sys.exit(1)
		install_php(args)
	else:
		print(f"Error: unknown command '{args.command}'", file=sys.stderr)
		parser.print_help()
		sys.exit(1)


if __name__ == "__main__":
	main()