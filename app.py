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

zone_name = config['App']['ZoneName']

app = Flask(__name__)

@app.route("/")
def index():
    res = requests.get('http://localhost:8080/list/required-modules')
    reqmods = json.loads(res.text)

    res = requests.get('http://localhost:8080/list/approved-instances')
    appinst = json.loads(res.text)

    res = requests.get('http://localhost:8080/list/prohibited-resources')
    probres = json.loads(res.text)

    res = requests.get('http://localhost:8080/list/can-delete')
    candelete = json.loads(res.text)

    return render_template("index.html", reqmods=reqmods, appinst=appinst, probres=probres, candelete=candelete)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
