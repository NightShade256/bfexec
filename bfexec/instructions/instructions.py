import enum


__all__ = ["InsType", "Instruction"]


class InsType(enum.Enum):
    """Defines BrainFuck operations."""

    # Standard BrainFuck Operations
    INCREMENT = "+"
    DECREMENT = "-"
    MRIGHT = ">"
    MLEFT = "<"
    WRITE = "."
    READ = ","
    JUMP_IF_ZERO = "["
    JUMP_UNLESS_ZERO = "]"

    # Optimizations
    CLEAR_LOOP = "C"
    SCAN_LOOP_L = "L"
    SCAN_LOOP_R = "R"


class Instruction:
    """Represents a BrainFuck operation."""

    def __init__(self, tp: InsType, value: int) -> None:
        self.tp = tp
        self.value = value

    def __str__(self) -> str:
        return f"<Instruction Type: {self.tp}, Value: {self.value}>"