from flask import Flask, session
from secrets import token_urlsafe

from .prefixmiddleware import PrefixMiddleWare

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(64)   # Way stronger than recommended but hey...
app.config['SESSION_TYPE'] = "redis"
app.wsgi_app = PrefixMiddleWare(app.wsgi_app, prefix='/api')