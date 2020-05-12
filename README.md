# bfexec

A simple BrainF**k interpreter written in Python.

## Installation

The preferred way to install bfexec is through pip

`pip install bfexec`

There is not going to be any compiled documentation for this.  
Instead please go through the source docstrings.

There are few BF programs in this repository in `/examples` (THEY ARE NOT MADE BY ME! ALL CREDIT TO THE CREATORS WHERE IT IS DUE!)
that you can run in my interpreter.

## Usage

You can use bfexec through the command line (assuming your Python Scripts folder is in PATH and Python interpreter
is set to open `.py` files)
(ONLY USE CMD on Windows! DO NOT USE POWERSHELL!)

`bf.py <filename here>`

Please only use files with `.bf` extension.

You can also import `bfexec` in your code and use it in your application.

Example:

```python
import bfexec
import sys

code = "SOME BF CODE"

interp = bfexec.BFInterpreter(code, sys.stdin, sys.stdout)
interp.run()
```

Instead of passing `sys.stdin` and `sys.stdout` to the BFInterpreter constructor, you can also
pass a StringIO instance or a File Object.

If you want to early exit a BF script that is running just, `Ctrl + C` (Keyboard Interrupt).

The interpreter actively optimizes for scan and clear loops.
But still the interpreter is quite SLOW.
The hanoi tower and mandelbrot set examples take excruciatingly long to finish.
This is in part due to Python itself being a interpreted language, and that
the interpreter doesn't optimize for other constructs.

I am trying to implement optimization for other constructs hence look out for that update!

## Contributing

Just open a pull request.

## Acknowledgements

This is inspired by an earlier BF interpreter written in Python that you can find [here](https://github.com/Shubbler/PyFuck).
I have added few of my own modifications that seek to make the interpreter better.

## License

This project is licensed under MIT license.

## Support

Please feel free to contact me on Discord, if you have any query regarding bfexec.
Username: `__NightShade256__#5169`
