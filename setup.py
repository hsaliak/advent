from setuptools import setup, find_packages
#from distutils.core import setup


setup(
    name="advent",
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
