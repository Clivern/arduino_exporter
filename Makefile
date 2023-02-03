PYTHON ?= python
PIP ?= $(PYTHON) -m pip
TOX ?= tox


help: Makefile
	@echo
	@echo " Choose a command run in Arduino Exporter:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo


## config: Install needed dependencies.
.PHONY: config
config:
	$(PIP) install twine
	$(PIP) install wheel
	$(PIP) install tox
	$(PIP) install setuptools-scm


## test: Run test case.
.PHONY: test
test:
	@echo "\n==> Run Test Cases:"
	$(TOX)


## ci: Run all CI checks.
.PHONY: ci
ci: test
	@echo "\n==> All quality checks passed"


## build: Build the package.
.PHONY: build
build:
	$(TOX) -e clean
	$(TOX) -e build


## version: Get latest version
.PHONY: version
version:
	$(PYTHON) setup.py --version


## release: Release to PyPi
release:
	$(PYTHON) -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*  --verbose


## install: Install the package locally
.PHONY: install
install:
	$(PYTHON) setup.py install


.PHONY: ci
