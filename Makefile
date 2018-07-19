# This is a Makefile, see
# https://www.gnu.org/software/make/manual/make.html#Introduction
# if you aren't already familiar

VENV_NAME = venv
APP_NAME = providers
VENV_PIP = $(VENV_NAME)/bin/pip
VENV_PYTHON = $(VENV_NAME)/bin/python
SYS_PYTHON3 = $(shell which python3)
DATA = Inpatient_Prospective_Payment_System__IPPS__Provider_Summary_for_the_Top_100_Diagnosis-Related_Groups__DRG__-_FY2011.csv

run: venv
	echo "App will run on localhost:5000"
	$(VENV_PYTHON) $(APP_NAME).py

venv:
	$(SYS_PYTHON3) -m pip install virtualenv
	virtualenv $(VENV_NAME)
	$(VENV_PIP) install -r requirements.txt

test: venv
	head -10 $(DATA) > test_data.csv
	$(VENV_NAME)/bin/pytest

load_data:
	echo "Must have app running"
	curl "localhost:5000/load_data"

clean:
	rm test_data.csv
	rm *.sqlite3
	rm *.log
	rm -rf $(VENV_NAME)
