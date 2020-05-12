import setuptools

setuptools.setup(
      name="bfexec",
      version="1.0.0",
      description="A simple BrainF**k interpreter written in Python.",
      license="MIT",
      author="Anish Jewalikar",
      author_email="anishjewalikar@gmail.com",
      scripts=["bfexec/bf.py"],
      py_modules=["bfexec"]
)