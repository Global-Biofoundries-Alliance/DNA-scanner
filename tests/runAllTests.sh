#!/bin/bash

echo "Initialize virtual Environment"
python3 -m venv venv

echo "Install dependencies"
./venv/bin/pip3 install -e ../Backend/
./venv/bin/pip3 install -r requirements.txt

echo "run tests"
venv/bin/python3 entitiestest.py -v
venv/bin/python3 validatortest.py -v
venv/bin/python3 compositepingertest.py -v
venv/bin/python3 geneartclienttest.py -v
venv/bin/python3 geneartpingertest.py -v
venv/bin/python3 idtclienttest.py -v
venv/bin/python3 idtpingertest.py -v
venv/bin/python3 controllertest.py -v
