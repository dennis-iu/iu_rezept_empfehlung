# Variablen
PYTHON_FILES := $(shell find . -type f -name "*.py" -not -path "./venv/*")
YAML_FILES := $(shell find . -type f -name "*.yml" -o -name "*.yaml")

# Projekt vorbereiten
prepare: create_virtualenv install_requirements
	@echo "Projekt ist jetzt bereit! Du kannst die main Methode ausführen."

# Virtuelle Python-Umgebung erstellen und aktivieren
create_virtualenv:
	@echo "Erstelle virtuelle Python-Umgebung..."
	python3 -m venv venv
	@echo "Aktiviere virtuelle Python-Umgebung..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		call venv\\Scripts\\activate; \
	elif [ "$(shell uname)" = "Darwin" ] || [ "$(shell uname)" = "Linux" ]; then \
		. venv/bin/activate; \
	else \
		echo "Unbekanntes Betriebssystem, keine Aktivierung der virtuellen Umgebung möglich."; \
	fi
	@echo "Virtuelle Python-Umgebung erstellt und aktiviert!"

# Installieren der Abhängigkeiten aus requirements.txt
install_requirements:
	@echo "Installiere Abhängigkeiten aus requirements.txt..."
	pip install -r requirements.txt
	@echo "Abhängigkeiten installiert!"

# make pre-commit Befehl erstellen
.PHONY: pre-commit
pre-commit: format-python fix-python fix-yaml update-requirements sync-dependencies
	@echo "Pre-commit checks and fixes successful!"

# Automatisch python Probleme fixen (flake8 mit autoflake + black + isort)
.PHONY: fix-python
fix-python:
	@echo "Fixing Python issues..."
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive $(PYTHON_FILES)
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Automatisch yaml Probleme fixen
.PHONY: fix-yaml
fix-yaml:
	@echo "Fixing YAML issues..."
	yamlfmt -w $(YAML_FILES)

# Update requirements.txt
.PHONY: update-requirements
update-requirements:
	@echo "Updating requirements.txt with current requirements.in..."
	pip-compile requirements.in

# Synchronisierung mit der requirements.txt
.PHONY: sync-dependencies
sync-dependencies:
	@echo "Syncing dependencies from requirements.txt..."
	pip-sync requirements.txt

# Alle Formatter und Prüfungen laufen lassen
.PHONY: format-python
format-python:
	@echo "Running Python formatters (black + isort)..."
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Optional
.PHONY: check-python
check-python:
	@echo "Running Python syntax check (flake8)..."
	flake8 $(PYTHON_FILES)

.PHONY: check-yaml
check-yaml:
	@echo "Running YAML syntax check (yamllint)..."
	yamllint $(YAML_FILES)
