import time
import typing

from bfexec.errors import BFRuntimeException
from bfexec.instructions import InsType


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
        self, program: list, stdin: typing.TextIO, stdout: typing.TextIO
    ) -> None:
        self.program = program
        self.cells = bytearray(30000)
        self.ip = 0
        self.dp = 0

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

        while self.ip < len(self.program):
            instruction = self.program[self.ip]

            if instruction.tp == InsType.INCREMENT:
                val = self.cells[self.dp]
                self.cells[self.dp] = ((val & 0xFF) + instruction.value) % 0x100
            elif instruction.tp == InsType.DECREMENT:
                val = self.cells[self.dp]
                self.cells[self.dp] = (
                    ((val & 0xFF) - instruction.value) % 0x100 + 0x100
                ) % 0x100
            elif instruction.tp == InsType.MLEFT:
                if self.dp - instruction.value < 0:
                    raise BFRuntimeException("[]index out of range")
                self.dp -= instruction.value
            elif instruction.tp == InsType.MRIGHT:
                if self.dp + instruction.value > 29999:
                    raise BFRuntimeException("[]index out of range")
                self.dp += instruction.value
            elif instruction.tp == InsType.WRITE:
                val = self.cells[self.dp]
                for _ in range(instruction.value):
                    self.stdout.write(chr(int(val)))
            elif instruction.tp == InsType.READ:
                for _ in range(instruction.value):
                    val = str(self.stdin.read(1))
                    if len(val) < 1 or ord(val) == 0:
                        self.cells[self.dp] = 0
                    else:
                        self.cells[self.dp] = ord(val)
            elif instruction.tp == InsType.JUMP_IF_ZERO:
                if self.cells[self.dp] == 0:
                    self.ip = instruction.value
            elif instruction.tp == InsType.JUMP_UNLESS_ZERO:
                if self.cells[self.dp] != 0:
                    self.ip = instruction.value
            elif instruction.tp == InsType.CLEAR_LOOP:
                self.cells[self.dp] = 0
            elif instruction.tp == InsType.SCAN_LOOP_L:
                while self.cells[self.dp] != 0:
                    if self.dp == 0:
                        raise BFRuntimeException("[]index out of range")
                    self.dp -= 1
            elif instruction.tp == InsType.SCAN_LOOP_R:
                while self.cells[self.dp] != 0:
                    if self.dp == 29999:
                        raise BFRuntimeException("[]index out of range")
                    self.dp += 1

            self.ip += 1

        end = time.perf_counter()
        delta = (end - start) * 10 ** 3

        if disp_time:
            self.stdout.write(f"\n\nExecution Time: {delta:.4f}ms.")

        return delta
