import logging
import os
import configparser
from flask import Flask
from flask import request
from flask_cors import CORS
from classes.CosmosData import CosmosData
from classes.SentinelData import SentinelData

#######################################
# Setup a few variables
#######################################

config = configparser.ConfigParser()
config.read('app.ini')
identifier = config['App']['Identifier']
account_key = config['App']['AccountKey']
data_source = CosmosData(account_key, identifier)
data = SentinelData(data_source)
app = Flask(__name__)
CORS(app)

#######################################
# Setup routes
#######################################

@app.route('/list/<list_name>/<provider>', strict_slashes=False, methods=['GET'])
def get_list(list_name, provider):
    return enlistor(list_name, get_value(request, 'add'), get_value(request, 'remove'), provider)

@app.route('/tags', strict_slashes=False, methods=['GET'])
def tags():
    return enlistor("mandatory-tags", get_value(request, 'add'), get_value(request, 'remove'), None)

@app.route('/ddb-encryption', strict_slashes=False, methods=['GET'])
def ddb_encryption():
    return evaluator("ddb-encryption", get_value(request, 'enable'))

@app.route('/no-star-access', strict_slashes=False, methods=['GET'])
def no_stars():
    return evaluator("no-star-access", get_value(request, 'enable'))

@app.route('/max-cost', strict_slashes=False, methods=['GET'])
def manage_cost():
    return evaluator("max-cost", get_value(request, 'cost'))

@app.route('/default-provider', strict_slashes=False, methods=['GET'])
def set_provider():
    return evaluator("default-provider", get_value(request, 'value'))

@app.route('/prevent-deletion', strict_slashes=False, methods=['GET'])
def set_del_policy():
    return evaluator("prevent-deletion", get_value(request, 'enable'))

@app.route('/reset', strict_slashes=False, methods=['GET'])
def reset_data():
    return data.reset_data()

#######################################
# Helper functions
#######################################

def evaluator(value, update):
    retval = ""
    if update:
        retval = data.set_value(value, update)
    else:
        retval = data.get_value(value)

    return retval

def enlistor(list_name, additem, delitem, provider):
    if additem:
        return data.add_to_list(list_name, additem, provider)
    elif delitem:
        return data.remove_from_list(list_name, delitem, provider)
    else:
        return data.get_list(list_name, provider)

def get_value(req, key):
    return req.args.get(key)

#######################################
# Let's get this puppy started!
#######################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
