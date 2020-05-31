import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="bfexec",
    version="1.0.3",
    description="A simple BrainF**k interpreter written in Python.",
    license="MIT",
    author="Anish Jewalikar",
    author_email="anishjewalikar@gmail.com",
    url="https://github.com/NightShade256/bfexec",
    scripts=["bfexec/bf.py"],
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
