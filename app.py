import logging
import os
import json
import configparser
from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

config = configparser.ConfigParser()
config.read('app.ini')

identifier = config['App']['Identifier']
account_name = identifier + "-cosmos-db"
account_key = config['App']['AccountKey']
table_endpoint = "https://" + identifier + "-cosmos-db.table.cosmos.azure.com:443/"
connection_string = "DefaultEndpointsProtocol=https;AccountName=" + account_name + ";AccountKey=" + account_key + ";TableEndpoint=" + table_endpoint + ";"
table_service = TableService(endpoint_suffix="table.cosmos.azure.com", connection_string=connection_string)
table_name = identifier + "-cosmos-table"

app = Flask(__name__)

@app.route("/")
def index():
    reqmods = [
        "custom-vnet",
        "custom-sg",
        "custom-blog"
    ]

    render_template("index.html", reqmods=reqmods)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
