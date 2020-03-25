#!/bin/bash

echo "Initialize virtual Environment"
python3 -m venv venv

echo "Install dependencies"
./venv/bin/pip3 install -e ../Backend/
./venv/bin/pip3 install -r requirements.txt

echo "run tests"
# Discover all tests and run them
venv/bin/coverage run -m unittest discover -p "*test.py"

# Just for Info: With the following command you can run a single test
# venv/bin/coverage run entitiestest.py -v

echo "show coverage"
venv/bin/coverage report --include='*Backend*' -m
