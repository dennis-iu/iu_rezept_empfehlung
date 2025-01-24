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
	@echo "Pre-commit erfolgreich!"

# Automatisch python Probleme fixen (flake8 mit autoflake + black + isort)
.PHONY: fix-python
fix-python:
	@echo "Python Probleme lösen..."
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive $(PYTHON_FILES)
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Automatisch yaml Probleme fixen
.PHONY: fix-yaml
fix-yaml:
	@echo "Yaml Probleme lösen..."
	yamlfmt -w $(YAML_FILES)

# Update requirements.txt
.PHONY: update-requirements
update-requirements:
	@echo "Updating requirements.txt mit der aktuellen requirements.in..."
	pip-compile requirements.in

# Synchronisierung mit der requirements.txt
.PHONY: sync-dependencies
sync-dependencies:
	@echo "Synchronisierung der Abhängigkeiten aus der requirements.txt..."
	pip-sync requirements.txt

# Alle Formatter und Prüfungen laufen lassen
.PHONY: format-python
format-python:
	@echo "Ausführung der Python Formatter (black + isort)..."
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Optional
.PHONY: check-python
check-python:
	@echo "Ausführung des Pyhton Syntax-Prüfers (flake8)..."
	flake8 $(PYTHON_FILES)

.PHONY: check-yaml
check-yaml:
	@echo "Ausführung des YAML Syntax-Prüfers(yamllint)..."
	yamllint $(YAML_FILES)
