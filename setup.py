#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(
  name='wtforms-html5',
  version=open('CHANGES.txt').readline().split()[0][1:-1],
  author='Brutus',
  author_email='brutus.dmc@googlemail.com',
  description='A Python module that adds HTML5 widgets to WTForms.',
  long_description=open('README.rst').read(),
  url='https://github.com/brutus/wtforms-html5/',
  download_url='https://github.com/brutus/wtforms-html5/zipball/master',
  license='LICENSE.txt',
  classifiers=[
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Internet :: WWW/HTTP'
  ],
  py_modules=['wtforms_html5', 'test_wtforms_html5'],
  requires=['wtforms']
)
