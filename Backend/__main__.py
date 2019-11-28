from flask import Flask
import sys
import optparse
import time

app = Flask(__name__)

@app.route('/ping')
def hello_world():
    return 'pong'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
