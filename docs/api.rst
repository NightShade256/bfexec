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
Make sure that the file has the extension ``.b`` or ``.bf``.

``bf <file name>.bf``

Compiler and VM
----------------

To use ``bfexec`` in your code, you must first compile the BrainF**ck code through the inbuilt compiler,
and then pass the compiled program to the VM. See the project README for an example.

.. autoclass:: bfexec.Compiler
    :members: compile_code

.. autoclass:: bfexec.BFInterpreter
    :members: run

Exceptions
-----------

.. autoexception:: bfexec.BFException

.. autoexception:: bfexec.BracketMismatch

.. autoexception:: bfexec.BFRuntimeException