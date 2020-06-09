# bfexec

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/97d726aca2da45709e8ec6c2375ecc44)](https://www.codacy.com/manual/anishjewalikar/bfexec?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NightShade256/bfexec&amp;utm_campaign=Badge_Grade)

A simple BrainF**k interpreter written in Python.

## Installation

The preferred way to install bfexec is through `pip`.

`pip install bfexec`

## Usage

You can use bfexec through the command line (assuming your Python Scripts folder is in PATH).
`bf <filename here>`

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

Please see the documentation for more.

You can find example BrainF**k programs in the `examples/` subdirectory.
All the credit for making the above mentioned programs go to there respective authors.

This interpreter is quite slow. You may notice that by running the Hanoi and Mandelbrot Set programs.
This is because the interpreter does no optimizations other than scan and clear loops.

## Changelog

v2.0.2

1. Added documentation through ReadTheDocs.

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
