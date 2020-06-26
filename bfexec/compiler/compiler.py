import re

from bfexec.errors import BracketMismatch
from bfexec.instructions import Instruction, InsType

RBF = re.compile(r"[^\+\-<>.,\[\]]")

# Clear Loop regex
RCL = re.compile(r"(\[-\])|(\[\+\])")

# Scan Loop regex
RSLR = re.compile(r"(\[>\])")
RSLL = re.compile(r"(\[<\])")

__all__ = ["Compiler"]


class Compiler:
    """A BrainFuck Compiler that emits instructions that can
    be run by the VM present in this package.

    Arguments
    ----------
    program : str
        The BrainFuck code that is to be compiled.
    """

    def __init__(self, program: str) -> None:
        # Compiler state variables.
        self.program = program
        self.instructions = []
        self.position = 0
        self.stack = []

        self.cleanup_code()
        self.program_len = len(self.program)

    def cleanup_code(self) -> None:
        """Cleanup the code of illegal characters."""
        self.program = RBF.sub("", self.program)
        self.program = RCL.sub("Z", self.program)
        self.program = RSLR.sub("R", self.program)
        self.program = RSLL.sub("L", self.program)

    def compile_code(self) -> list:
        """Compile the code into instructions.

        Returns
        --------
        list
            A list of instructions that can be interpreted by the VM.
        """
        while self.position < self.program_len:
            current = self.program[self.position]

            if current == "+":
                self.collapse_instruction(current, InsType.INCREMENT)
            elif current == "-":
                self.collapse_instruction(current, InsType.DECREMENT)
            elif current == "<":
                self.collapse_instruction(current, InsType.MLEFT)
            elif current == ">":
                self.collapse_instruction(current, InsType.MRIGHT)
            elif current == ".":
                self.collapse_instruction(current, InsType.WRITE)
            elif current == ",":
                self.collapse_instruction(current, InsType.READ)
            elif current == "[":
                ins_pos = self.new_instruction(InsType.JUMP_IF_ZERO, 0)
                self.stack.append(ins_pos)
            elif current == "]":
                if not self.stack:
                    raise BracketMismatch(self.position, "]")
                open_ins = self.stack[-1]
                self.stack.pop()
                close_ins = self.new_instruction(InsType.JUMP_UNLESS_ZERO, open_ins)
                self.instructions[open_ins].value = close_ins
            elif current == "Z":
                self.new_instruction(InsType.CLEAR_LOOP, 1)
            elif current == "R":
                self.new_instruction(InsType.SCAN_LOOP_R, 1)
            elif current == "L":
                self.new_instruction(InsType.SCAN_LOOP_L, 1)

            self.position += 1

        if self.stack:
            raise BracketMismatch(self.stack.pop(), "[")

        # Compile loops and return the compiled list.
        return self.instructions

    def collapse_instruction(self, char: str, tp: InsType) -> None:
        """Collapse repeated operations into a single instruction."""
        count = 1
        while (
            self.position < self.program_len - 1
            and self.program[self.position + 1] == char
        ):
            count += 1
            self.position += 1

        self.new_instruction(tp, count)

    def new_instruction(self, tp: InsType, value: int) -> int:
        """Append a new instruction to the instruction list."""
        ins = Instruction(tp, value)
        self.instructions.append(ins)
        return len(self.instructions) - 1
