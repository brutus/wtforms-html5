#!/usr/bin/env python
from codecs import open

from setuptools import setup


VERSION = "0.4.0"

DESCRIPTION = "Generates render keywords for widgets of WTForms HTML5 fields."

INSTALL_REQUIRES = [
    "wtforms",
]


def read_file(filename):
    """Returns the contents of *filename* (UTF-8)."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()


setup(
    name="wtforms-html5",
    version=VERSION,
    package_dir={"": "src"},
    py_modules=["wtforms_html5"],
    requires=["wtforms"],
    install_requires=INSTALL_REQUIRES,
    author="Brutus",
    author_email="brutus.dmc@googlemail.com",
    description=DESCRIPTION,
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/brutus/wtforms-html5/",
    download_url="https://github.com/brutus/wtforms-html5/zipball/master",
    license="GNU GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
