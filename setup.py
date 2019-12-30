from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="advent",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    ext_modules = cythonize("machine.pyx", annotate=True)
)
