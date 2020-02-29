import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest

        sys.exit(pytest.main(shlex.split(self.pytest_args)))


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="coinoxr",
    version="0.0.1",
    description="Python client for Open Exchange Rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Calado",
    license="MIT",
    author_email="me@luiscalado.eu",
    packages=["coinoxr"],
    install_requires=["requests >= 2.20"],
    python_requires=">=3.5",
    cmdclass={"test": PyTest},
    tests_require=[
        "pytest >= 5.3",
        "pytest-mock >= 2.0",
        "pytest-cov >= 2.8",
        "coverage >= 5.0",
    ],
)
