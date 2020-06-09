import argparse
import sys

from bfexec import BFInterpreter


def main() -> None:

    # Create CLI argument parser.
    parser = argparse.ArgumentParser("Execute BF code.")
    parser.add_argument(
        "file_name", metavar="file", type=str, help="Path to the BF file."
    )

    args = parser.parse_args()

    # Check if the file is actually a BF file.
    if not args.file_name.endswith(".bf"):
        print("Unrecognized file extension. Only use .bf files.")
        return

    # Try to open the file and run.
    try:
        with open(args.file_name) as fp:
            code = fp.read()
    except FileNotFoundError:
        return print(f"File {args.file_name} does not exist.")
    interp = BFInterpreter(code, sys.stdin, sys.stdout)
    try:
        interp.run()
    except KeyboardInterrupt:
        print("^C Keyboard Interrupt encountered. Exiting...")
