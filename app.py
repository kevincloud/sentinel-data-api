import logging
import os
import json
import configparser
import requests
from flask import Flask
from flask import render_template
from flask_cors import CORS

config = configparser.ConfigParser()
config.read('app.ini')

app = Flask(__name__)

@app.route("/")
def index():
    res = requests.get('http://localhost:8080/list/required-modules')
    reqmods = json.loads(res)
    # reqmods = [
    #     "custom-vnet",
    #     "custom-sg",
    #     "custom-blog"
    # ]

    return render_template("index.html", reqmods=reqmods)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
