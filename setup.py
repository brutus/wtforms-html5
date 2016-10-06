#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals

import os

from codecs import open
from setuptools import setup

from wtforms_html5 import __version__, __doc__


INSTALL_REQUIRES = [
  'wtforms',
]

EXTRAS_REQUIRE = {
  'test': [
    'werkzeug',
    'beautifulsoup4',
  ],
  'dev': [
    'bumpversion',
    'flake8',
    'pylint',
  ],
}


def get_short_description(text):
  """
  Returns the first paragraph from *text*.

  """
  return [p.strip() for p in text.strip().split('\n\n')][0]


def read_file(filename, paths=[]):
  """
  Returns the contents of *filename* (UTF-8).

  If *paths* is set, join those before the *fielname*.

  """
  if paths:
    paths.append(filename)
    filename = os.path.join(*paths)
  with open(filename, encoding='utf-8') as f:
    return f.read()


setup(
  name='wtforms-html5',
  version=__version__,
  py_modules=['wtforms_html5'],
  requires=['wtforms'],
  install_requires=INSTALL_REQUIRES,
  extras_require=EXTRAS_REQUIRE,
  author='Brutus',
  author_email='brutus.dmc@googlemail.com',
  description=get_short_description(__doc__),
  long_description=read_file('README.rst'),
  url='https://github.com/brutus/wtforms-html5/',
  download_url='https://github.com/brutus/wtforms-html5/zipball/master',
  license='GNU GPLv3',
  classifiers=[
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Internet :: WWW/HTTP'
  ],
)
