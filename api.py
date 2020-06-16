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
CORS(app)

@app.route('/list/<list_name>/<provider>', strict_slashes=False, methods=['GET'])
def get_list(list_name, provider):
    logging.info('Started function get_list()')

    policylist = list_name
    additem = get_value(request, 'add')
    delitem = get_value(request, 'remove')

    listvalues = []
    if policylist:
        try:
            items = table_service.query_entities(table_name, filter="PartitionKey eq '" + policylist + "'")
        except ValueError:
            pass
        else:
            for item in items:
                if str(item.RowKey).endswith(provider):
                    listvalues.append(str(item.RowKey).replace("|" + provider, ""))
    else:
        return json.dumps(listvalues)
    
    if additem:
        if add_item(policylist, additem, provider):
            listvalues.append(additem)
        else:
            return json.dumps(listvalues)
    
    if delitem:
        if remove_item(policylist, delitem, provider):
            listvalues.remove(delitem)
        else:
            return json.dumps(listvalues)
    
    return json.dumps(listvalues)

@app.route('/set-provider', strict_slashes=False, methods=['GET'])
def set_provider():
    provider = get_value(request, 'provider')
    update_item("default-provider", provider)

    return '{ "status": "ok" }'

@app.route('/deletion-policy', strict_slashes=False, methods=['GET'])
def set_del_policy():
    value = get_value(request, 'value')
    update_item("prevent-deletion", value)

    return '{ "status": "ok" }'

@app.route('/can-delete', strict_slashes=False, methods=['GET'])
def can_delete():
    retval = "false"
    try:
        items = table_service.query_entities(table_name, filter="PartitionKey eq 'prevent-deletion'")
    except ValueError:
        retval = "false"
    else:
        for item in items:
            retval = item.RowKey
    
    if retval != "true":
        retval = "false"
    
    return '{ "prevent-deletion": "' + retval + '" }'

@app.route('/default-provider', strict_slashes=False, methods=['GET'])
def get_def_provider():
    retval = "azurerm"
    try:
        items = table_service.query_entities(table_name, filter="PartitionKey eq 'default-provider'")
    except ValueError:
        retval = "azurerm"
    else:
        for item in items:
            retval = item.RowKey
    
    if retval is None:
        retval = "azurerm"
    
    return '{ "default-provider": "' + retval + '" }'

@app.route('/reset', strict_slashes=False, methods=['GET'])
def reset_data():
    data_set = {
        "required-modules": [
            "custom-vnet|azurerm",
            "custom-sg|azurerm",
            "custom-blob|azurerm",
            "custom-vpc|aws",
            "custom-sg|aws",
            "custom-s3|aws"
        ],
        "approved-instances": [
            "Standard_A1_v2|azurerm",
            "Standard_A2_v2|azurerm",
            "Standard_A4_v2|azurerm",
            "Standard_A8_v2|azurerm",
            "t3.micro|aws",
            "t3.small|aws",
            "t3.medium|aws",
            "t3.large|aws"
        ],
        "prohibited-resources": [
            "azurerm_resource_group|azurerm",
            "azurerm_virtual_network|azurerm",
            "azurerm_network_security_group|azurerm",
            "azurerm_subnet_network_security_group_association|azurerm"
        ],
        "prevent-deletion": [
            "true"
        ],
        "default-provider": [
            "azurerm"
        ]
    }

    # delete all entries
    items = table_service.query_entities(table_name)
    for itm in items:
        table_service.delete_entity(table_name, itm.PartitionKey, itm.RowKey)

    # add all entries
    for category in data_set:
        for value in data_set[category]:
            item = Entity()
            item.PartitionKey = category
            item.RowKey = value
            table_service.insert_entity(table_name, item)

    return '{ "status": "ok" }'

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

def get_value(req, key):
    return req.args.get(key)

def update_item(key, value):
    item = Entity()
    item.PartitionKey = key
    item.RowKey = value

    old_value = ""
    try:
        entries = table_service.query_entities(table_name, filter="PartitionKey eq '" + key + "'")
    except ValueError:
        old_value = ""
    else:
        for entry in entries:
            old_value = entry.RowKey
    
    try:
        table_service.delete_entity(table_name, key, old_value)
    except ValueError:
        return False

    try:
        table_service.insert_entity(table_name, item)
    except ValueError:
        return False
    
    return True

def add_item(listname, value, provider):
    item = Entity()
    item.PartitionKey = listname
    item.RowKey = value + '|' + provider
    try:
        table_service.insert_entity(table_name, item)
    except ValueError:
        return False
    
    return True

def remove_item(listname, value, provider):
    try:
        table_service.delete_entity(table_name, listname, value + '|' + provider)
    except ValueError:
        return False
    
    return True



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
