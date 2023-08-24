VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
ACTIVATE = $(VENV)/bin/activate
STATIC = app/static
GUNICORN = $(VENV)/bin/gunicorn

.PHONY: production development clean static

production:
	$(GUNICORN) --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app

development:
	$(PYTHON) MaD.py

install: static venv

static: 
	cd $(STATIC); npm install

venvc: clean $(VENV)/bin/activate

venv: $(VENV)/bin/activate
	$(PYTHON) -m ensurepip --upgrade
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)

clean:
	rm -rf $(VENV)
	find -iname "*.pyc" -delete
	rm -rf __pycache__
