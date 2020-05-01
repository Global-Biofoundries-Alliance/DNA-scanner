'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
from secrets import token_urlsafe

from flask import Flask, session

from .prefixmiddleware import PrefixMiddleWare


app = Flask(__name__)
# Way stronger than recommended but hey...
app.config['SECRET_KEY'] = token_urlsafe(64)
app.config['SESSION_TYPE'] = "redis"
app.wsgi_app = PrefixMiddleWare(app.wsgi_app, prefix='/api')
