import argparse
import sys

from bfexec import BFInterpreter, Compiler


def main() -> None:

    # Create CLI argument parser.
    parser = argparse.ArgumentParser("Execute BF code.")
    parser.add_argument("file", metavar="file", type=str, help="Path to the BF file.")

    args = parser.parse_args()

    # Check if the file is actually a BF file.
    if not args.file.endswith((".b", ".bf")):
        return print("Unrecognized file extension. Only use .b and .bf files.")

    # Try to open the file and run.
    try:
        with open(args.file) as fp:
            code = fp.read()
    except FileNotFoundError:
        return print(f"File {args.file} does not exist.")

    compiler = Compiler(code)
    program = compiler.compile_code()
    interp = BFInterpreter(program, sys.stdin, sys.stdout)
    try:
        interp.run(True)
    except KeyboardInterrupt:
        print("KeyboardInterrupt encountered. Quitting...")
