import json

#######################################
# SentinelData is intended to be an
# interface, which allows any type 
# of data source to be used.
#######################################

class SentinelData:
    # Retrieve the data source
    def __init__(self, data_source):
        self.data_source = data_source
    
    # Get a list
    def get_list(self, list_name, provider):
        return json.dumps(self.data_source.get_list(list_name, provider))
    
    # Add an item to a list
    def add_to_list(self, list_name, provider, value):
        return json.dumps(self.data_source.add_to_list(list_name, provider, value))

    # Remove an item from a list
    def remove_from_list(self, list_name, provider, value):
        return json.dumps(self.data_source.remove_from_list(list_name, provider, value))

    # Get a value from a K/V pair
    def get_value(self, key):
        return '{ "' + key + '": "' + self.data_source.get_value(key) + '" }'
    
    # Set a new value for a K/V pair
    def set_value(self, key, value):
        status = "ok"
        if not self.data_source.set_value(key, value):
            status = "error"

        return '{ "status": "' + status + '" }'
    
    # Remove all data and load in the default data
    def reset_data(self):
        status = "ok"
        if not self.data_source.data_load():
            status = "error"
        
        return '{ "status": "' + status + '" }'
