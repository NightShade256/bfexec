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
        self.compile_multiply_loops()
        self.match_braces()
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

    # Credit: Matslina on Github.
    def compile_multiply_loops(self):
        """Compile Multiply Loops"""

        # Copy the list.
        ir = self.instructions[:]

        i = 0
        while True:

            # Find a loop, that doesn't contain any other loop.
            while i < len(ir):
                if ir[i].tp == InsType.JUMP_IF_ZERO:
                    break

                i += 1
            else:
                break

            j = i + 1
            while j < len(ir):
                if ir[j].tp == InsType.JUMP_UNLESS_ZERO:
                    break

                if ir[j].tp == InsType.JUMP_IF_ZERO:
                    i = j

                j += 1
            else:
                break

            # Check if the loop only contains +, -, <, > operations.
            if (
                set(op.tp for op in ir[i + 1 : j])
                - set(
                    [
                        InsType.INCREMENT,
                        InsType.DECREMENT,
                        InsType.MLEFT,
                        InsType.MRIGHT,
                    ]
                )
                != set()
            ):
                i = j
                continue

            # Interpret the loop and track pointer position.
            mem, p = {}, 0
            for op in ir[i + 1 : j]:
                if op.tp == InsType.INCREMENT:
                    mem[p] = mem.get(p, 0) + op.value
                elif op.tp == InsType.DECREMENT:
                    mem[p] = mem.get(p, 0) - op.value
                elif op.tp == InsType.MRIGHT:
                    p += op.value
                elif op.tp == InsType.MLEFT:
                    p -= op.value

            # If pointer is at the starting position, and only 1
            # is subtracted from Cell 0 then this is a multiply/copy loop.
            if p != 0 or mem.get(0, 0) != -1:
                i = j
                continue

            mem.pop(0)

            instblock = [Instruction(InsType.MULT_LOOP, mem[p], offset=p) for p in mem]
            ir = ir[:i] + instblock + [Instruction(InsType.CLEAR_LOOP, 1)] + ir[j + 1 :]

        self.instructions = ir

    def match_braces(self) -> None:
        """This has to be done once again since we destroyed the earlier scheme."""

        stack = []

        for pos, op in enumerate(self.instructions):
            if op.tp == InsType.JUMP_IF_ZERO:
                stack.append(pos)
            elif op.tp == InsType.JUMP_UNLESS_ZERO:
                inst_pos = stack.pop()

                # Patch the Open Inst with Close pos.
                inst = self.instructions[inst_pos]
                inst.value = pos
                self.instructions[inst_pos] = inst

                # Patch the Close Inst with Open pos.
                inst = self.instructions[pos]
                inst.value = inst_pos
                self.instructions[pos] = inst
