import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("photon_observer/__init__.py", "r") as f:
    version = str(ast.literal_eval(_version_re.findall(f.read())[0]))

requirements = [
    # To keep things simple, we only support newer versions of Graphene
    "pyshark",
    "pydantic<2",
]
tests_require = [
    "pytest>7.0",
    "pytest-cov"
]

setup(
    name="photon_observer",
    version=version,
    description="Tools for working with the Photon protocol",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MyrikLD/photon_observer",
    author="Yorsh Sergey",
    author_email="myrik260138@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="photon binary protocol",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    extras_require={
        "test": tests_require,
    },
    tests_require=tests_require,
)
