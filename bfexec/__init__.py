"""A BrainF**k interpreter written in Python.

It is a basic interpreter which tries to optimize
for scan and clear loops.
"""

from .bf import *

__all__ = [
    "BFInterpreter",
    "BFError",
    "BracketMatchError",
    "RunTimeError"
]

__author__ = "Anish Jewalikar"
__version__ = "1.0.3"
__license__ = "MIT"