__all__ = ["BFException", "BracketMismatch", "BFRuntimeException"]


class BFException(Exception):
    """Base exception class for bfexec.
    This can be caught to handle any exception thrown from this library."""

    pass


class BracketMismatch(BFException):
    """Exception that is thrown when there is a mismatch in the square brackets.
    Attributes
    ----------
    index : int
        The position of the erring bracket in the cleaned up source
        code.
    bracket_type : str
        The type of the erring bracket, that is: one of ``[``, ``]``.
    """

    def __init__(self, index: int, bracket_type: str):
        self.index = index
        self.bracket_type = bracket_type


class BFRuntimeException(BFException):
    """Exception thrown when there is a runtime error."""

    pass
