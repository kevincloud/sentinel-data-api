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
    res = requests.get('http://localhost:8080/default-provider')
    obj = json.loads(res.text)
    defprovider = obj["default-provider"]

    res = requests.get('http://localhost:8080/list/required-modules/' + defprovider)
    reqmods = json.loads(res.text)

    res = requests.get('http://localhost:8080/list/approved-instances/' + defprovider)
    appinst = json.loads(res.text)

    res = requests.get('http://localhost:8080/list/prohibited-resources/' + defprovider)
    probres = json.loads(res.text)

    res = requests.get('http://localhost:8080/can-delete')
    obj = json.loads(res.text)
    candelete = obj["prevent-deletion"]

    return render_template("index.html", reqmods=reqmods, appinst=appinst, probres=probres, candelete=candelete, defprovider=defprovider)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
