.PHONY: all setup exe tests
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYINSTALLER = venv/Scripts/pyinstaller.exe
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYINSTALLER = ./venv/bin/pyinstaller
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

PIP = $(PYTHON) -m pip install

SOURCE = source
TESTS = tests

PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
LINT = $(PYTHON) -m pylint  --init-hook="sys.path.insert(0, './')" --load-plugins=pylint.extensions.mccabe --max-complexity=10

all: run

cmd_sweep:
	$(PYTHON) $(SOURCE)/cli.py sweep --addres=192.168.1.100 --video=10 --freq_center=1450000000 --rbw=2 --atten=0

cmd_read:
	$(PYTHON) $(SOURCE)/cli.py read --addres=192.168.1.100 --freq_start=1400000000 --freq_end=1400330000 --video=50 --rbw=0 --atten=0 --with_data

cmd_long:
	$(PYTHON) $(SOURCE)/cli.py read

exe:
	$(PYINSTALLER) --onefile --name satis.exe $(SOURCE)/cli.py

test:
	$(PTEST) -s $(TESTS)/test/$(T)

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(LINT) $(TESTS)/test
	$(LINT) $(SOURCE)

pep257:
	$(PYTHON) -m pep257 $(SOURCE)
	$(PYTHON) -m pep257 --match='.*\.py' $(TESTS)/test

radon:
	$(PYTHON) -m radon cc $(TESTS)/test -s -a -nc --no-assert
	$(PYTHON) -m radon cc $(SOURCE) -s -a -nc

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r $(TESTS)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
