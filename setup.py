#!/usr/bin/env python3

from setuptools import setup, find_packages
import singleton_decorator

setup(
    name = "singleton_decorator",
    version = singleton_decorator.__version__,
    fullname = "Singleton Decorator",
    description = "A testable singleton decorator",
    author = "Taras Gaidukov",
    author_email = "kemaweyan@gmail.com",
    keywords = "singleton decorator unittest",
    long_description = open('README.rst').read(),
    url = "https://github.com/Kemaweyan/singleton_decorator",
    license = "GPLv3",
    packages=find_packages(exclude=["*.tests"])
)
