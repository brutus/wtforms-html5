.PHONY: \
	setup setup-venv setup-requirements setup-pre-commit \
	upgrade freeze \
	lint \
	doctest unittest coverage tests tests-recreate \
	change clog \
	release \
	clean full-clean build publish


setup: setup-venv setup-requirements setup-pre-commit

setup-venv: version ?= 3.9
setup-venv:
	python$(version) -m venv .venv
	.venv/bin/pip install --isolated --no-input --quiet --upgrade pip

setup-requirements: req ?= requirements.txt
setup-requirements:
	.venv/bin/pip install --isolated --no-input --quiet -r '$(req)'

setup-pre-commit:
	.venv/bin/pre-commit install --overwrite --install-hooks


upgrade:
	.venv/bin/pip install --upgrade \
	$(shell .venv/bin/pip list --outdated | awk 'NR>2 {print $$1}')

freeze:
	.venv/bin/pip freeze > requirements.prod.txt


lint:
	.venv/bin/pre-commit run --all-files


doctests:
	.venv/bin/python -m xdoctest --quiet wtforms_html5

unittests:
	.venv/bin/python -m unittest discover

coverage:
	.venv/bin/coverage run --append --source wtforms_html5 -m unittest discover
	.venv/bin/coverage report -m

tests:
	.venv/bin/tox

tests-recreate:
	.venv/bin/tox --recreate


change: slug ?= $(shell tr -dc A-Za-z0-9 < /dev/urandom | head -c9)
change:
	.venv/bin/reno new $(slug)

clog: version ?= $(shell git describe | awk -F'-g' '{print $$1}')
clog:
	.venv/bin/reno report --title='CHANGELOG' --version '$(version)' 2>/dev/null


release: part ?= patch
release:
	$(eval version = $(shell \
		.venv/bin/bumpversion --dry-run --allow-dirty --list $(part) \
		| grep '^current_version=' \
		| cut -d= -f2 \
	))
	$(eval new = $(shell \
		.venv/bin/bumpversion --dry-run --allow-dirty --list $(part) \
		| grep '^new_version=' \
		| cut -d= -f2 \
	))
	@echo "bump $(part) -> $(version) => $(new)"
	@git tag '$(new)'
	.venv/bin/reno report --no-show-source --title=CHANGELOG --output=CHANGELOG.rst 2>/dev/null
	@git tag -d '$(new)'
	git add CHANGELOG.rst
	if ! git diff --staged --exit-code; then \
		git commit -m ':memo: update CHANGELOG for $(new)' --no-verify; \
	fi
	.venv/bin/bumpversion '$(part)' --commit-args='--no-verify'


clean:
	rm -rf build dist

full-clean: clean
	rm -rf .venv .tox


build: clean
	.venv/bin/python -m build


publish: build
	.venv/bin/python -m twine check dist/*
	.venv/bin/python -m twine upload dist/*
