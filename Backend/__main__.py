'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
import optparse
import sys
import time

from flask import Flask

from Controller import routes
from Controller.app import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
