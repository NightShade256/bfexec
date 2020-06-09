"""A BrainF**k interpreter written in Python.

It is a basic interpreter which tries to optimize
for scan and clear loops.
"""

from .bf import BFInterpreter
from .errors import BFException, BracketMismatch, BFRuntimeException

__all__ = ["BFInterpreter", "BFException", "BracketMismatch", "BFRuntimeException"]

__author__ = "Anish Jewalikar"
__version__ = "2.0.0"
__license__ = "MIT"
