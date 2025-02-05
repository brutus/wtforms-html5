.PHONY: \
	clean full-clean \
	lint check fmt \
	tests doctests coverage \
	build publish \
	change clog \
	release

clean:
	rm -rf MANIFEST build dist

full-clean: clean
	rm -rf .venv .tox .nox .pytest_cache .mypy_cache .ruff_cache .coverage*

# LINTING

lint:
	hatch run lint:pc

check:
	hatch run lint:check

fix:
	hatch run lint:fix
	hatch run lint:upgrade

# TESTS

test:
	hatch test

coverage:
	hatch test --cover

version-test:
	hatch test --all --cover

doctest:
	hatch test -- --xdoctest src/

# PACKAGING

build: clean
	hatch build --clean --target wheel

publish: build
	hatch publish

# CHANGELOG

CHANGE_TYPES := rm fix feat change

change: issue ?= _$(shell < /dev/urandom tr -dc A-Za-z0-9 | head -c9)
change: change_file := changes/$(issue).$(type).md
change:
ifneq ($(filter $(type),$(CHANGE_TYPES)),)
	touch '$(change_file)'
	$(EDITOR) '$(change_file)'
else
	@echo "Given change type '$(type)' is not a suported value: $(CHANGE_TYPES)"
endif

clog:
	hatch run project:towncrier build --draft --version Unreleased


# RELEASE

RELEASE_LEVELS := patch minor major

release:
ifneq ($(filter $(part),$(RELEASE_LEVELS)),)
	# check git status
	@if ! git diff-index --quiet HEAD; then \
		echo "ERROR: git unclean!"; \
		exit 1; \
	fi
	# get next version (for changelog)
	$(eval new_version := $(shell \
	  hatch run project:bumpver update --dry --$(part) 2>&1 \
	  | grep 'New Version:' \
	  | awk '{print $$NF}' \
	))
	@echo "bump -> '$(new_version)'"
	# write changelog
	hatch run project:towncrier build --yes --version '$(new_version)'
	if ! git diff --staged --exit-code; then \
		git commit -m 'chore: add CHANGELOG for `$(new_version)`' --no-verify; \
	fi
	# bump version
	hatch run project:bumpver update '--$(part)'
else
	@echo "Given part '$(part)' is not a suported value: $(RELEASE_LEVELS)"
endif
