import logging
import os
import json
import configparser
from flask import Flask
from flask import request
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

@app.route('/list/<list_name>', strict_slashes=False, methods=['GET'])
def get_list(list_name):
    logging.info('Started function get_list()')

    policylist = list_name
    additem = get_value(request, 'add')
    delitem = get_value(request, 'remove')

    listvalues = []
    if policylist:
        items = table_service.query_entities(table_name, filter="PartitionKey eq '" + policylist + "'")
        for item in items:
            listvalues.append(item.RowKey)
    else:
        return json.dumps(listvalues)
    
    if additem:
        if add_item(policylist, additem):
            listvalues.append(additem)
        else:
            return json.dumps(listvalues)
    
    if delitem:
        if remove_item(policylist, delitem):
            listvalues.remove(delitem)
        else:
            return json.dumps(listvalues)
    
    return json.dumps(listvalues)

def get_value(request, key):
    retval = request.params.get(key)
    if not retval:
        try:
            req_body = request.get_json()
        except ValueError:
            pass
        else:
            retval = req_body.get(key)
    return retval

def add_item(listname, value):
    item = Entity()
    item.PartitionKey = listname
    item.RowKey = value
    try:
        table_service.insert_entity(table_name, item)
    except ValueError:
        return False
    
    return True

def remove_item(listname, value):
    try:
        table_service.delete_entity(table_name, listname, value)
    except ValueError:
        return False
    
    return True

def get_value(req, key):
    return req.args.get(key)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
