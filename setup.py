from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymztab-m-IaaIaaSPDR",
    version="0.0.2",
    author="Nils Hoffmann",
    author_email="nils.hoffmann@isas.de",
    description="The Python3 language bindings for mzTab-M",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lifs-tools/pymzTab-m",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    python_requires='>=3.5'
)

