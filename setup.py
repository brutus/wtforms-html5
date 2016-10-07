#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals

import os

from codecs import open
from setuptools import setup


VERSION = '0.2.2'

DESCRIPTION = 'Generates render keywords for widgets of WTForms HTML5 fields.'

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


def read_file(filename, prepend_paths=[]):
  """
  Returns the contents of *filename* (UTF-8).

  If *prepend_paths* is set, join those before the *fielname*.
  If it is `True`, prepend the path to `setup.py`.

  """
  if prepend_paths is True:
    prepend_paths = [
      os.path.abspath(os.path.dirname(__file__)),
    ]
  if prepend_paths:
    prepend_paths.append(filename)
    filename = os.path.join(*prepend_paths)
  print(filename)
  with open(filename, encoding='utf-8') as f:
    return f.read()


setup(
  name='wtforms-html5',
  version=VERSION,
  py_modules=['wtforms_html5'],
  requires=['wtforms'],
  install_requires=INSTALL_REQUIRES,
  extras_require=EXTRAS_REQUIRE,
  author='Brutus',
  author_email='brutus.dmc@googlemail.com',
  description=DESCRIPTION,
  long_description=read_file('README.md'),
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
