import re
import typing

from bfexec.errors import BracketMismatch
from bfexec.instructions import Instruction, InstructionType

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
        self.instructions: typing.List[Instruction] = []
        self.position = 0

        self.cleanup_code()
        self.program_len = len(self.program)

    def cleanup_code(self) -> None:
        """Cleanup the code of illegal characters."""
        self.program = RBF.sub("", self.program)
        self.program = RCL.sub("Z", self.program)
        self.program = RSLR.sub("R", self.program)
        self.program = RSLL.sub("L", self.program)

    def compile_code(self) -> typing.List[Instruction]:
        """Compile the code into instructions.

        Returns
        --------
        list
            A list of instructions that can be interpreted by the VM.
        """
        if self.program.count("[") != self.program.count("]"):
            if self.program.count("[") > self.program.count("]"):
                raise BracketMismatch(self.program.index("["), "[")
            else:
                raise BracketMismatch(self.program.rindex("]"), "]")

        while self.position < self.program_len:
            current = self.program[self.position]

            if current == "+":
                self.collapse_instruction(current, InstructionType.Arithmetic)
            elif current == "-":
                self.collapse_instruction(
                    current, InstructionType.Arithmetic, negative=True
                )
            elif current == "<":
                self.collapse_instruction(
                    current, InstructionType.Pointer, negative=True
                )
            elif current == ">":
                self.collapse_instruction(current, InstructionType.Pointer)
            elif current == ".":
                self.collapse_instruction(current, InstructionType.Write)
            elif current == ",":
                self.collapse_instruction(current, InstructionType.Read)
            elif current == "[":
                # Emit instruction with a bogus value.
                # Patch it after compilation of multiply loops.
                self.new_instruction(InstructionType.JumpRight, 0)
            elif current == "]":
                self.new_instruction(InstructionType.JumpLeft, 0)
            elif current == "Z":
                self.new_instruction(InstructionType.Clear, 0)
            elif current == "R":
                self.new_instruction(InstructionType.ScanRight, 0)
            elif current == "L":
                self.new_instruction(InstructionType.ScanLeft, 0)

            self.position += 1

        # Compile loops and match brackets.
        self.compile_multiply_loops()
        self.match_brackets()

        return self.instructions

    def collapse_instruction(
        self, char: str, tp: InstructionType, **args: bool
    ) -> None:
        """Collapse repeated operations into a single instruction."""

        count = 1
        while (
            self.position < self.program_len - 1
            and self.program[self.position + 1] == char
        ):
            count += 1
            self.position += 1

        self.new_instruction(tp, count, **args)

    def new_instruction(self, tp: InstructionType, value: int, **args: bool) -> int:
        """Append a new instruction to the instruction list."""

        if args.get("negative", False):
            ins = Instruction(tp, -value)
        else:
            ins = Instruction(tp, value)

        self.instructions.append(ins)
        return len(self.instructions) - 1

    # Credit: Matslina on Github.
    def compile_multiply_loops(self):
        """Compile Multiply Loops"""

        allowed_set = set((InstructionType.Arithmetic, InstructionType.Pointer,))
        empty_set = set()

        # Copy the list.
        ir: typing.List[Instruction] = self.instructions[:]

        i = 0
        while True:

            # Find a loop, that doesn't contain any other loop.
            while i < len(ir):
                if ir[i].tp == InstructionType.JumpRight:
                    break

                i += 1
            else:
                break

            j = i + 1
            while j < len(ir):
                if ir[j].tp == InstructionType.JumpLeft:
                    break

                if ir[j].tp == InstructionType.JumpRight:
                    i = j

                j += 1
            else:
                break

            # Check if the loop only contains +, -, <, > operations.
            if set(op.tp for op in ir[i + 1 : j]) - allowed_set != empty_set:
                i = j
                continue

            # Interpret the loop and track pointer position.
            mem: typing.Dict[int, int] = {}
            p = 0

            for op in ir[i + 1 : j]:
                if op.tp == InstructionType.Arithmetic:
                    mem[p] = mem.get(p, 0) + op.value
                elif op.tp == InstructionType.Pointer:
                    p += op.value

            # If pointer is at the starting position, and only 1
            # is subtracted from Cell 0 then this is a multiply/copy loop.
            if p != 0 or mem.get(0, 0) != -1:
                i = j
                continue

            mem.pop(0)

            instblock = [
                Instruction(InstructionType.Multiply, mem[p], offset=p) for p in mem
            ]
            ir = (
                ir[:i]
                + instblock
                + [Instruction(InstructionType.Clear, 0)]
                + ir[j + 1 :]
            )

        self.instructions = ir

    def match_brackets(self) -> None:
        """Match brackets in the compiled instructions."""

        stack = []

        for pos, op in enumerate(self.instructions):
            if op.tp == InstructionType.JumpRight:
                stack.append(pos)
            elif op.tp == InstructionType.JumpLeft:
                right_pos = stack.pop()

                # Patch the Open Inst with Close pos.
                self.instructions[right_pos].value = pos

                # Patch the Close Inst with Open pos.
                self.instructions[pos].value = right_pos
