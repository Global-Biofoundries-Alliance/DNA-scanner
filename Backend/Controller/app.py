from flask import Flask
from secrets import token_urlsafe

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(64);   # Way stronger than recommended but hey...

