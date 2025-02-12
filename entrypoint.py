import argparse
import subprocess
import sys
import re
from pathlib import Path

VALID_CLANG_FORMAT_OPTIONS = [
    f"clang-format{x}"
    for x in ("5", "6", "7", "8", "9", "10", "11", "11.0.0", "11.1.0", "12", "12.0.0", "12.0.1", "13", "13.0.0", "14", "14.0.0", "15", "15.0.2", "16", "16.0.0", "16.0.3", "17", "17.0.4", "18", "18.1.3", "18.1.8")
]

def run_clang_format(clang_format_exe: Path, style: str, inplace: bool, regex: str):
    """Runs clang-format on specified files."""
    if not clang_format_exe.exists():
        raise FileNotFoundError(f"Cannot locate clang-format at location:\n\t'{clang_format_exe}'")
    args = [str(clang_format_exe), f"--style={style}"]

    if inplace:
        args.append("-i")

    files = [f for f in Path(".").rglob("*") if f.is_file()]

    if regex:
        regex_pattern = re.compile(regex)
        files = [str(f) for f in files if regex_pattern.search(str(f))]

    if not files:
        print(f"No files matched the regex: {regex}")
        sys.exit(1)

    args += files

    print(f"Running command:\n\t{' '.join(args)}")

    try:
        subprocess.run(args, check=True)
        print("clang-format completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: clang-format failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: {clang_format_exe} not found. Ensure the correct version is installed.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run clang-format with specified options.")
    parser.add_argument("--executable", type=Path, default="", help="Specify clang-format executable (e.g., 'clang-format18').")
    parser.add_argument("--style", type=str, default="file", help="Formatting style (default: 'file').", choices=("file", "LLVM", "GNU", "Google", "Chromium", "Microsoft", "Mozilla", "WebKit"))
    parser.add_argument("--inplace", action="store_true", help="Modify files in place.")
    parser.add_argument("--regex", type=str, default=r"^.*\.(c|h|C|H|cpp|hpp|cc|hh|c++|h++|cxx|hxx)$", help="Regex pattern to filter files.")
    args = parser.parse_args()

    if args.executable.name not in VALID_CLANG_FORMAT_OPTIONS:
        parser.error(f"Executable '{args.executable.name}' not in valid options ({','.join(VALID_CLANG_FORMAT_OPTIONS)})")

    run_clang_format(args.executable, args.style, args.inplace, args.regex)
