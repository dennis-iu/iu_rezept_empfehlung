# variables
PYTHON_FILES := $(shell find . -type f -name "*.py" -not -path "./venv/*")
YAML_FILES := $(shell find . -type f -name "*.yml" -o -name "*.yaml")

# build make pre-commit command
.PHONY: pre-commit
pre-commit: check-python check-yaml format-python update-requirements sync-dependencies
	@echo "Pre-commit checks successful!"

# python syntax check with flake8
.PHONY: check-python
check-python:
	@echo "Starting python syntax check with flake8"
	flake8 $(PYTHON_FILES)

# yaml syntax check with yamllint
.PHONY: check-yaml
check-yaml:
	@echo "Starting yaml syntax check with yamllint"
	yamllint $(YAML_FILES)

# pep 8 conform python formatting
.PHONY: format-python
format-python:
	@echo "Starting pep 8 conform python formatting with black and isort"
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# update requirements.txt
.PHONY: update-requirements
update-requirements:
	@echo "Updating requirements.txt with current requirements.in"
	pip-compile requirements.in

# sync requirements.txt
.PHONY: sync-dependencies
sync-dependencies:
	@echo "Syncing dependencies from requirements.txt"
	pip-sync requirements.txt
