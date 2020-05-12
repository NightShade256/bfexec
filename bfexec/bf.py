import argparse
import re
import sys
import time
from io import StringIO

OPERATORS_MAP = {
    "<": "move_left",
    ">": "move_right",
    "+": "increment",
    "-": "decrement",
    ".": "write",
    ",": "read",
    "[": "jump_if_zero",
    "]": "jump_unless_zero",
    "Z": "zero_loop",
    "R": "scan_loop_right",
    "L": "scan_loop_left"
}

# Code regex
RBF = re.compile(r"[^\+\-<>.,\[\]]")

# Zero Loop regex
RZL = re.compile(r"(\[-\])|(\[\+\])")

# Scan Loop regex
RSLR = re.compile(r"(\[>\])")
RSLL = re.compile(r"(\[<\])")

class BFError(Exception):
    """Base exception for all the other exceptions."""
    pass


class BracketMatchError(BFError):
    """Raised when there is a mismatch in the square brackets.

    Attributes
    ----------
    index : int
        The position of the erring bracket in the cleaned_up source
        code.
    bracket_type : str
        The type of the erring bracket, ie: one of ``[``, ``]``.
    """

    def __init__(self, index: int, bracket_type: str):
        self.index = index
        self.bracket_type = bracket_type


class RunTimeError(BFError):
    """Raised when there is a run time error."""
    pass


def fetch_bracket_map(code: str) -> tuple:
    """Returns the bracket map.

    Arguments
    ---------
    code : str
        The code whose bracket map to fetch.

    Returns
    -------
    tuple
        The bracket map.
    """

    heap = []
    bracket_map = {}

    for pos, op in enumerate(code):
        if op == "[":
            heap.append(pos)
        elif op == "]":
            if not heap:
                raise BracketMatchError(index=pos, bracket_type="]")
            bracket_map[heap.pop()] = pos

    if heap:
        raise BracketMatchError(index=heap.pop(), bracket_type="[")

    return bracket_map

def optimize_code(code: str) -> str:
    """Optimizes the code a little bit."""

    optimized = RZL.sub("Z", code)
    optimized = RSLR.sub("R", optimized)
    optimized = RSLL.sub("L", optimized)
    return optimized

def build_code(code: str):
    cleaned_code = RBF.sub("", code)
    optimized_code = optimize_code(cleaned_code)
    return optimized_code

class BFInterpreter:
    """A simple BrainF**k interpreter.

    Arguments
    ---------
    code : str
        The BrainF**k code that is to be executed.
    stdin : StringIO
        The input stream, can be a file can be sys.stdin
    stdout : StringIO
        The output stream, can be a file can be sys.stdout
    """

    def __init__(self, code: str, stdin: StringIO, stdout: StringIO):
        self.tape: list = [0 for _ in range(30000)]
        self.code = build_code(code)
        self.program_pointer = 0
        self.pointer = 0
        self.stdin = stdin
        self.stdout = stdout
        self.bracket_map = fetch_bracket_map(self.code)
        self.inv_map = {v: k for k, v in self.bracket_map.items()}

    def move_left(self) -> None:
        """Moves the pointer left by `times`."""
        if self.pointer - 1 < 0:
            raise RunTimeError("[] Index out of range.")
        self.pointer -= 1

    def move_right(self) -> None:
        """Moves the pointer right by `times`."""
        if self.pointer + 1 > 29999:
            raise RunTimeError("[] Index out of range")
        self.pointer += 1

    def increment(self) -> None:
        """Increments the value by `times` at the cell under the pointer.

        Value 255 wraps to 0."""
        val = self.tape[self.pointer]
        self.tape[self.pointer] = ((val & 0xFF) + 1) % 0x100

    def decrement(self) -> None:
        """Decrements the value by times at the cell under the pointer.

        Value 0 wraps to 255."""
        val = self.tape[self.pointer]
        self.tape[self.pointer] = (((val & 0xFF) - 1) % 0x100 + 0x100) % 0x100

    def write(self) -> None:
        """Writes the value of the cell under the pointer in the buffer.

        The buffer can be stdout or a StringIO object."""

        self.stdout.write(chr(self.tape[self.pointer]))

    def read(self) -> None:
        """Reads one byte from the buffer.

        The buffer can be stdin or a StringIO object."""
        byte = self.stdin.read(1)
        if len(byte) < 1 or ord(byte) == 0:
            self.tape[self.pointer] = 0
        else:
            self.tape[self.pointer] = ord(byte)

    def jump_if_zero(self) -> None:
        """Jumps to the closing bracket if the current cell value is zero."""
        if self.tape[self.pointer] == 0:
            try:
                self.program_pointer = self.bracket_map[self.program_pointer]
            except KeyError as e:
                raise RuntimeError(str(e))

    def jump_unless_zero(self) -> None:
        """Jump to the opening bracket unless current cell value is zero."""
        if self.tape[self.pointer] != 0:
            try:
                self.program_pointer = self.inv_map[self.program_pointer]
            except KeyError as e:
                raise RunTimeError(str(e))
    
    def zero_loop(self) -> None:
        """Sets the cell under the pointer to 0."""
        self.tape[self.pointer] = 0
    
    def scan_loop_left(self) -> None:
        """Runs a scan loop to the left."""
        while self.tape[self.pointer] != 0:
            if self.pointer == 0:
                raise RunTimeError("[] Index out of range.")
            self.pointer -=1
    
    def scan_loop_right(self) -> None:
        """Runs a scan loop to the right."""
        while self.tape[self.pointer] != 0:
            if self.pointer == 29999:
                raise RunTimeError("[] Index out of range.")
            self.pointer +=1

    def run(self, disp_time: bool = True) -> float:
        """Interpret the BF code.

        Arguments
        ---------
        disp_time : bool
            Whether to display the total time it took to execute the code.

        Returns
        -------
        float
            The total time in milliseconds it took to execute the code.

        Raises
        ------
        RunTimeError : If there is a runtime error.
        """
        start = time.perf_counter()

        while True:
            try:
                op = self.code[self.program_pointer]
            except IndexError:
                break

            # Get the corresponding function.
            attr = OPERATORS_MAP[op]
            func = getattr(self, attr)

            if func():
                func()

            self.program_pointer += 1

        end = time.perf_counter()

        if disp_time:
            self.stdout.write(f"\n\nFinished in {((end-start)*1000):.4f}ms.")

        return (end-start)*1000


def main():

    # Create CLI argument parser.
    parser = argparse.ArgumentParser("Execute BF code.")
    parser.add_argument("file_name", metavar="file",
                        type=str, help="Path to the BF file.")

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

if __name__ == "__main__":
    main()
