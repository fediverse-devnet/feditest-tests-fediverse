#
# make venv
#     Create a python environment for your platform and install the required dependencies int
#     it. It will be in ./venv.$(uname -s)
#
# make build
#     run pip install in your venv
#
# make lint
#     Run several linters on the code
#
# make test
#     Run unit tests
#
# NOTE: This does not add the venv to your $PATH. You have to do that yourself if you want that.
#

UNAME?=$(shell uname -s | tr [A-Z] [a-z])
BRANCH?=$(shell git branch --show-current)
VENV?=venv.$(UNAME).$(BRANCH)
PYTHON?=python3.11
FEDITEST?=$(VENV)/bin/feditest -v
DOMAIN?=--domain 1234.lan

# FEDITEST_BRANCH?=$(shell cd ../feditest && git branch --show-current)
# FEDITEST_VENV=../feditest/venv.$(UNAME).$(FEDITEST_BRANCH)

default : lint

all : lint

build : venv
	$(VENV)/bin/pip install .

venv : $(VENV)

$(VENV) :
	@which $(PYTHON) || ( echo 'No executable called "python". Append your python to the make command, like "make PYTHON=your-python"' && false )
	$(PYTHON) -mvenv $(VENV)
	$(VENV)/bin/pip install ruff mypy pylint

lint : build
	$(VENV)/bin/ruff check tests ../feditest/src
	MYPYPATH='tests ../feditest/src' $(VENV)/bin/mypy --namespace-packages --explicit-package-bases --install-types --non-interactive tests ../feditest/src
	@# These options should be the same flags as in .pre-commit-config.yml, except that I can't get it to
	@# work there without the "--ignore-missing-imports" flag, while it does work without it here
	@# MYPYPATH is needed because apparently some type checking ignores the directory option given as command-line argument

.PHONY: all default venv build lint
