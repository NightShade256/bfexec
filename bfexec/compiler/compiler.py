import re

from bfexec.errors import BracketMismatch
from bfexec.instructions import Instruction, InsType

RBF = re.compile(r"[^\+\-<>.,\[\]]")


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
        self.program_len = len(self.program)
        self.instructions = []
        self.position = 0
        self.stack = []

    def cleanup_code(self) -> None:
        """Cleanup the code of illegal characters."""
        self.program = RBF.sub("", self.program)

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

            self.position += 1

        if self.stack:
            raise BracketMismatch(self.stack.pop(), "[")

        # Compile loops and return the compiled list.
        return self.compile_loops(self.instructions)

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

    def compile_loops(self, instruction_list: list) -> list:
        """Compile loops into Instructions."""
        for count, inst in enumerate(instruction_list):
            if inst.tp == InsType.JUMP_IF_ZERO:
                if (
                    instruction_list[count + 1].tp == InsType.DECREMENT
                    and instruction_list[count + 2] == InsType.JUMP_UNLESS_ZERO
                ):
                    instruction_list[count] == Instruction(InsType.CLEAR_LOOP, 1)
                elif (
                    instruction_list[count + 1].tp == InsType.MLEFT
                    and instruction_list[count + 2] == InsType.JUMP_UNLESS_ZERO
                ):
                    instruction_list[count] == Instruction(InsType.SCAN_LOOP_L, 1)
                elif (
                    instruction_list[count + 1].tp == InsType.MRIGHT
                    and instruction_list[count + 2] == InsType.JUMP_UNLESS_ZERO
                ):
                    instruction_list[count] == Instruction(InsType.SCAN_LOOP_R, 1)

        return instruction_list
