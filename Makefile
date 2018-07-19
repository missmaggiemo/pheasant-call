# This is a Makefile, see
# https://www.gnu.org/software/make/manual/make.html#Introduction
# if you aren't already familiar

VENV_NAME = venv
APP_NAME = providers
VENV_PIP = $(VENV_NAME)/bin/pip
VENV_PYTHON = $(VENV_NAME)/bin/python
SYS_PYTHON3 = $(shell which python3)

run: venv
	echo "App will run on localhost:5000"
	$(VENV_PYTHON) $(APP_NAME).py

venv:
	$(SYS_PYTHON3) -m pip install virtualenv
	virtualenv $(VENV_NAME)
	$(VENV_PIP) install -r requirements.txt

load_data:
	echo "Must have app running"
	curl "localhost:5000/load_data"

clean:
	rm -rf $(VENV_NAME)

.PHONY: clean load_data run
