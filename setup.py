from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='designofexperiment',
    version='1.1.2',
    description='A Python Package for intuitive design of experiments with user-friendly analysis of results',
    py_modules=["design"],
    package_dir={'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "numpy == 1.19.1",
        "pandas == 1.1.1"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.1",
            "check-manifest>=0.42",
            "twine>=3.2.0"
        ],
    },
    url="https://github.com/JamesMarshall31/design-of-experiments",
    author="James Marshall, Benedict Carling",
    author_email="jm7618@ic.ac.uk, bencarling1@gmail.com"
)
