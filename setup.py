from setuptools import setup, find_packages

setup(name="advent", packages=find_packages(), 
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'])


