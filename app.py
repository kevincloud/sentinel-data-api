import json
import requests
from flask import Flask
from flask import render_template
from flask_cors import CORS

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

    res = requests.get('http://localhost:8080/list/allowed-resources/' + defprovider)
    allres = json.loads(res.text)

    res = requests.get('http://localhost:8080/tags')
    tags = json.loads(res.text)

    res = requests.get('http://localhost:8080/prevent-deletion')
    obj = json.loads(res.text)
    candelete = obj["prevent-deletion"]

    res = requests.get('http://localhost:8080/max-cost')
    obj = json.loads(res.text)
    maxcost = obj["max-cost"]

    res = requests.get('http://localhost:8080/ddb-encryption')
    obj = json.loads(res.text)
    ddbenc = obj["ddb-encryption"]

    res = requests.get('http://localhost:8080/no-star-access')
    obj = json.loads(res.text)
    nostar = obj["no-star-access"]

    return render_template("index.html", 
        reqmods=reqmods, 
        appinst=appinst, 
        probres=probres, 
        allres=allres,
        candelete=candelete, 
        defprovider=defprovider,
        maxcost=maxcost,
        tags=tags,
        ddbenc=ddbenc,
        nostar=nostar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
