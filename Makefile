# Makefile for managing a Python virtual environment

VENV_NAME = python-api
PYTHON = python3
VENV = $(PYTHON) -m venv

.PHONY: venv create activate deactivate

venv: activate ## Create and activate virtual environment

create: ## Create virtual environment
	$(VENV) $(VENV_NAME)

activate: ## Activate virtual environment
	@echo "Activating virtual environment..."
ifeq ($(OS),Windows_NT)
	.\$(VENV_NAME)\Scripts\activate
else
	@echo "Make sure to run 'source $(VENV_NAME)/bin/activate' in your terminal."
	@bash -c "source $(VENV_NAME)/bin/activate; exec bash"
endif

deactivate: ## Deactivate virtual environment
	@echo "Deactivating virtual environment..."
ifeq ($(OS),Windows_NT)
	@deactivate
else
	@deactivate
endif
