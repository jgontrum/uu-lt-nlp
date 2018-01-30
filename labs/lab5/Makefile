.PHONY: clean start build-and-push test

TAG=$(shell git symbolic-ref -q --short HEAD)

all: env/bin/python

env/bin/python:
	virtualenv env -p python3.6 --no-site-packages
	env/bin/pip install --upgrade pip
	env/bin/pip install wheel
	env/bin/pip install -r requirements.txt

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts .cache .scannerwork
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage
	rm -fv logs/*.txt
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
