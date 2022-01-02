# Changelog

All notable changes to this project will be documented in this file. The format
is based on [Keep a Changelog][], and this project adheres to
[Semantic Versioning][].

You can find the **issue tracker** at:
<https://github.com/brutus/wtforms-html5/issues>

[keep a changelog]: https://keepachangelog.com/
[semantic versioning]: https://semver.org/

<!-- TOWNCRIER -->

## v0.4.0 (2019-05-24)

All around update.

### Added Features

-   ✨ Added support for `maxlenght` and `minlength`. **Thanks** to
    [Gowee](https://github.com/Gowee). Closing [Issue
    4](https://github.com/brutus/wtforms-html5/issues/4).

-   ✅ Added tested support for Python `3.6` and `3.7`.

### Changes

-   📦 Added _Pipfile_ for [Pipenv](https://github.com/pypa/pipenv).

-   🚨 Use [autopep8](https://github.com/hhatto/autopep8) for automatic
    formatting.

-   📝 Use [reno](https://pypi.org/project/reno/) for CHANGELOG generation.

### Updates

-   🏗 Updated `Makefile`.

-   📝 Updated docs.

-   👽 New import path for `MultiDict` from
    [Werkzeug](https://palletsprojects.com/p/werkzeug/).

### Removed

-   🔥 Removed old `CHANGES.md`.

### Misc

-   👥 Added new contributor: [Gowee](https://github.com/Gowee) - Thanks!

## v0.3.0 (2016-12-16)

Small code re-factoring.

### Changes

-   ♻️ Put each auto–setting in it's own function.

-   📦 Changed linting tool-set from
    [flake8](http://flake8.pycqa.org/en/latest/) and
    [pylint](https://www.pylint.org/) to
    [pylama](https://github.com/klen/pylama).

### Updates

-   📝 Updated the docs.

## v0.2.4 (2016-11-10)

### Updates

-   📝 Updated the docs.

## v0.2.3 (2016-10-08)

### Updates

-   👷 Added some polish to the `Makefile` and CI.

-   📝 Improved the docs.

## v0.2.2 (2016-10-07)

### Fixes

-   📝 Added `setup.py` to bumpversion configuration.

## v0.2.1 (2016-10-07)

Makefile and automation.

### Added Features

-   🏗 Added Makefile.

-   🚨 Added style check command (PEP–8…).

-   ✅ Test coverage analysis with [Coveralls](https://coveralls.io/).

-   👷 [Travis CI](https://travis-ci.org/) integration.

-   👷 [Landscape](https://landscape.io/) integration.

### Changes

-   📝 New `CHANGELOG` format.

### Updates

-   📝 Updated Docs and added badges.

### Removed

-   🔥 Removed `run…` files and replaced them with a `makefile`.

## v0.2.0 (2016-10-06)

Huge re-factoring. Dropping all fields, widgets and validators and include a new
meta class for forms instead. See [README.md](README.md) for more information.

### Added Features

-   ✅ Configured [tox](https://tox.readthedocs.io/) for automated testing.

-   📦 Added requirement files.

### Changes

-   ♻️ Use _meta class_ for forms.

-   ✅ Use plain _unittest_ instead of _nosetest_.

### Updates

-   ➕ Added dependencies to `setup.py`.

### Removed

-   🔥 Removed all fields, widgets and validators.

-   📦 Removed tests from the Python package.

## v0.1.2 (2012-11-12)

### Added Features

-   ✅ Added test cases.

## v0.1.1 (2012-11-11)

### Fixes

-   📝 Fixed some spelling errors in the documentation.

## v0.1.0 (2012-11-10)

🎉 Initial release.
