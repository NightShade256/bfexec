.. currentmodule:: bfexec

bfexec documentation
=====================

Installation
-------------

You can install bfexec on all platforms through ``pip``.

``pip install -U bfexec``

Usage in terminal
------------------

You can run BrainF**k files in the console very easily.
Make sure that the file has the extension ``.bf``.

``bf <file name>.bf``

BFInterpreter
--------------

.. autoclass:: bfexec.BFInterpreter
    :members: run

Exceptions
-----------

.. autoexception:: bfexec.BFException

.. autoexception:: bfexec.BracketMismatch

.. autoexception:: bfexec.BFRuntimeException