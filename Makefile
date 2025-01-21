# Variables
PYTHON_FILES := $(shell find . -type f -name "*.py" -not -path "./venv/*")
YAML_FILES := $(shell find . -type f -name "*.yml" -o -name "*.yaml")

# Projekt vorbereiten
prepare: create_virtualenv install_requirements
	@echo "Projekt ist jetzt bereit! Du kannst die main Methode ausführen."

# Virtuelle python Umgebung erstellen
create_virtualenv:
	@echo "Erstelle virtuelle Python-Umgebung..."
	python3 -m venv venv
	@echo "Virtuelle Umgebung erstellt!"

# Installieren der Abhängigkeiten aus requirements.txt
install_requirements:
	@echo "Installiere Abhängigkeiten aus requirements.txt..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		call venv\\Scripts\\activate && pip install -r requirements.txt; \
	elif [ "$(shell uname)" = "Darwin" ] || [ "$(shell uname)" = "Linux" ]; then \
		. venv/bin/activate && pip install -r requirements.txt; \
	else \
		echo "Unbekanntes Betriebssystem, keine Abhängigkeitsinstallation möglich."; \
		exit 1; \
	fi
	@echo "Abhängigkeiten installiert!"

# Build make pre-commit command
.PHONY: pre-commit
pre-commit: format-python fix-python fix-yaml update-requirements sync-dependencies
	@echo "Pre-commit checks and fixes successful!"

# Automatically fix Python issues (flake8 with autoflake + black + isort)
.PHONY: fix-python
fix-python:
	@echo "Fixing Python issues..."
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive $(PYTHON_FILES)
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Fix YAML formatting with yamlfmt
.PHONY: fix-yaml
fix-yaml:
	@echo "Fixing YAML issues..."
	yamlfmt -w $(YAML_FILES)

# Update requirements.txt
.PHONY: update-requirements
update-requirements:
	@echo "Updating requirements.txt with current requirements.in..."
	pip-compile requirements.in

# Sync dependencies with requirements.txt
.PHONY: sync-dependencies
sync-dependencies:
	@echo "Syncing dependencies from requirements.txt..."
	pip-sync requirements.txt

# Run all formatters and checks
.PHONY: format-python
format-python:
	@echo "Running Python formatters (black + isort)..."
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Optional: Include check targets for validation (e.g., to run in CI/CD)
.PHONY: check-python
check-python:
	@echo "Running Python syntax check (flake8)..."
	flake8 $(PYTHON_FILES)

.PHONY: check-yaml
check-yaml:
	@echo "Running YAML syntax check (yamllint)..."
	yamllint $(YAML_FILES)
