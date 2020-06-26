# bfexec

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/97d726aca2da45709e8ec6c2375ecc44)](https://www.codacy.com/manual/anishjewalikar/bfexec?utm_source=github.com&utm_medium=referral&utm_content=NightShade256/bfexec&utm_campaign=Badge_Grade)

A simple BrainF\*\*k interpreter written in Python.

## Installation

The preferred way to install bfexec is through `pip`.

`pip install -U bfexec`

## Usage

You can use bfexec through the command line (assuming your Python Scripts folder is in PATH).
`bf <filename here>`

Please only use files with `.b` or `.bf` extension.

You can also import `bfexec` in your code and use it in your application.

Example:

```python
import sys

import bfexec


code = "SOME BF CODE"


compiler = bfexec.Compiler(code)
program = compiler.compile_code()
interp = bfexec.BFInterpreter(program, sys.stdin, sys.stdout)
interp.run()
```

Please see the documentation for more.

You can find example BrainF\*\*k programs in the `examples/` subdirectory.
All the credit for making the above mentioned programs go to there respective authors.

This interpreter is quite slow. You may notice that by running the Hanoi and Mandelbrot Set programs.
This is because Python itself is an interpreted language, and there are massive overheads in function calls
dropping off the performance.

## Changelog

v3.0.0

1. Massively overhaul backend code. The interpreter now collapses repeating instructions and compiles them to special format.
   This format can then be executed by a VM that is present in the package that should lead to some performance boosts for larger
   programs. Smaller programs may not benefit at all from this change or may even take longer to execute due to the compile time
   overhead.

2. Change the library interface. This is a breaking change.

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
