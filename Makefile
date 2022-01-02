.PHONY: \
	setup setup-venv setup-requirements setup-pre-commit \
	clean full-clean upgrade \
	lint audit \
	all-tests unittests doctests coverage \
	change clog \
	release build publish


PYTHON_VERSION := $(shell cat runtime.txt)

RELEASE_LEVELS := patch minor major


# SETUP

setup: setup-venv setup-requirements setup-pre-commit

setup-venv: version ?= $(cat runtime.txt)
setup-venv:
	python$(PYTHON_VERSION) -m venv --clear --upgrade-deps .venv

export PATH := $(shell pwd)/.venv/bin:$(PATH)

setup-requirements: req ?= requirements.txt
setup-requirements:
	pip install --isolated --no-input --quiet -r '$(req)'

setup-pre-commit:
	pre-commit install --install-hooks

clean:
	rm -rf MANIFEST build dist

full-clean: clean
	rm -rf .venv .tox .nox .pytest_cache .mypy_cache .coverage*

upgrade:
	pip-compile \
		--upgrade \
		--no-header \
		--strip-extras \
		--annotation-style line \
		--output-file requirements/constraints.txt \
		setup.cfg \
		requirements/*.in


# LINTING

lint:
	pre-commit run --all-files

audit:
	safety check --file requirements/constraints.txt


# TESTS

all-tests:
	tox $(args)

doctests:
	xdoctest --quiet wtforms_html5

unittests:
	python -m unittest discover

coverage:
	coverage erase
	coverage run -m unittest discover $(args)
	coverage report


# CHANGELOG

change: issue ?= _$(shell < /dev/urandom tr -dc A-Za-z0-9 | head -c9)
change: type ?= feature
change: change_file := changes/$(issue).$(type).md
change:
	touch '$(change_file)'
	$(EDITOR) '$(change_file)'

clog:
	towncrier --draft --version=Unreleased


# PACKAGING

release:
ifneq ($(filter $(part),$(RELEASE_LEVELS)),)
	$(eval version = $(shell \
		bumpversion --dry-run --allow-dirty --list $(part) \
		| grep '^current_version=' \
		| cut -d= -f2 \
	))
	$(eval new = $(shell \
		bumpversion --dry-run --allow-dirty --list $(part) \
		| grep '^new_version=' \
		| cut -d= -f2 \
	))
	@echo "bump $(part) -> $(version) => $(new)"
	towncrier --yes --version '$(new)'
	if ! git diff --staged --exit-code; then \
		git commit -m ':memo: add CHANGELOG for $(new)' --no-verify; \
	fi
	bumpversion '$(part)' --commit-args='--no-verify'
else
	@echo "Given part '$(part)' is not a suported value: $(RELEASE_LEVELS)"
endif

build: clean
	python -m build

publish: build
	python -m twine check dist/*
	python -m twine upload dist/*
