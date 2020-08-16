import time
import typing

from bfexec.errors import BFRuntimeException
from bfexec.instructions import Instruction, InstructionType


__all__ = ["BFInterpreter"]


class BFInterpreter:
    """A simple BrainFuck interpreter.

    Arguments
    ---------
    program : list
        The compiled BrainFuck program (compiled by the inbuilt compiler)
        that is to be executed.
    stdin : TextIO
        The input stream, this can be a file or ``sys.stdin``.
    stdout : TextIO
        The output stream, this can be a file or ``sys.stdout``.
    """

    def __init__(
        self,
        program: typing.List[Instruction],
        stdin: typing.TextIO,
        stdout: typing.TextIO,
    ) -> None:
        self.program = program
        self.program_length = len(program)

        self.cells = bytearray(30000)
        self.ip: int = 0
        self.dp: int = 0

        self.stdin = stdin
        self.stdout = stdout

    def run(self, disp_time: bool = False) -> float:
        """Interpret the BrainFuck code.

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
        BFRuntimeError
            If there is a runtime error.
        """

        start = time.perf_counter()

        while self.ip < self.program_length:
            instruction = self.program[self.ip]

            if instruction.tp == InstructionType.Arithmetic:
                self.cells[self.dp] = (
                    ((self.cells[self.dp] & 0xFF) + instruction.value) % 0x100 + 0x100
                ) % 0x100
            elif instruction.tp == InstructionType.Pointer:
                self.dp += instruction.value
            elif instruction.tp == InstructionType.Write:
                val = self.cells[self.dp]
                for _ in range(instruction.value):
                    self.stdout.write(chr(int(val)))
            elif instruction.tp == InstructionType.Read:
                for _ in range(instruction.value):
                    val = str(self.stdin.read(1))
                    if len(val) < 1 or ord(val) == 0:
                        self.cells[self.dp] = 0
                    else:
                        self.cells[self.dp] = ord(val)
            elif instruction.tp == InstructionType.JumpRight:
                if self.cells[self.dp] == 0:
                    self.ip = instruction.value
            elif instruction.tp == InstructionType.JumpLeft:
                if self.cells[self.dp] != 0:
                    self.ip = instruction.value
            elif instruction.tp == InstructionType.Clear:
                self.cells[self.dp] = 0
            elif instruction.tp == InstructionType.ScanLeft:
                index = self.cells.rfind(0, 0, self.dp + 1)

                if index == -1:
                    raise BFRuntimeException("[]index out of range")

                self.dp = index
            elif instruction.tp == InstructionType.ScanRight:
                index = self.cells.find(0, self.dp, 30000)

                if index == -1:
                    raise BFRuntimeException("[]index out of range")

                self.dp = index
            elif instruction.tp == InstructionType.Multiply:
                self.cells[self.dp + instruction.offset] = (
                    (self.cells[self.dp + instruction.offset] & 0xFF)
                    + (self.cells[self.dp] * instruction.value)
                ) % 0x100

            self.ip += 1

        end = time.perf_counter()
        delta = (end - start) * 10 ** 3

        if disp_time:
            self.stdout.write(f"\n\nExecution Time: {delta:.4f}ms.")

        return delta
