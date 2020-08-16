"""
Contains definition of an Instruction, and its types.
"""

import enum


__all__ = ["Instruction", "InstructionType"]


class InstructionType(enum.Enum):
    """Defines a set of operations."""

    # Standard BrainFuck Operations
    Arithmetic = 0
    Pointer = 1
    Read = 2
    Write = 3
    JumpRight = 4
    JumpLeft = 5

    # Optimizations
    Clear = 6
    ScanLeft = 7
    ScanRight = 8
    Multiply = 9


class Instruction:
    """Represents a BrainFuck operation."""

    def __init__(self, tp: InstructionType, value: int, **kwargs: int) -> None:
        self.tp = tp
        self.value = value
        self.offset: int = kwargs.get("offset", 0)

    def __str__(self) -> str:
        return f"<Instruction Type: {self.tp}, Value: {self.value}>"
