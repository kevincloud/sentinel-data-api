from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

#######################################
# CosmosData is a data source for 
# Azure's Cosmos DB Table. To be used 
# with the SentinelData interface.
#######################################

class CosmosData:
    # Setup initial variables
    def __init__(self, account_key, identifier):
        self.account_key = account_key
        self.identifier = identifier
        self.account_name = self.identifier + "-cosmos-db"
        self.table_endpoint = "https://" + self.identifier + "-cosmos-db.table.cosmos.azure.com:443/"
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=" + self.account_name + ";AccountKey=" + self.account_key + ";TableEndpoint=" + self.table_endpoint + ";"
        self.table_service = TableService(endpoint_suffix="table.cosmos.azure.com", connection_string=self.connection_string)
        self.table_name = self.identifier + "-cosmos-table"

    # Get a list of values
    def get_list(self, list_name, provider = None):
        pkey = ""
        if provider is not None:
            pkey = "|" + provider
        main_list = []
        if list_name:
            try:
                items = self.table_service.query_entities(self.table_name, filter="PartitionKey eq '" + list_name + "'")
            except ValueError:
                pass
            else:
                for item in items:
                    if str(item.RowKey).endswith(provider):
                        main_list.append(str(item.RowKey).replace(pkey, ""))

        return main_list

    # Add a value to a list
    def add_to_list(self, list_name, value, provider = None):
        pkey = ""
        if provider is not None:
            pkey = "|" + provider
        item = Entity()
        item.PartitionKey = list_name
        item.RowKey = value + pkey
        main_list = self.get_list(list_name)
        try:
            self.table_service.insert_entity(self.table_name, item)
        except ValueError:
            pass
        else:
            main_list.append(value)
        
        return main_list

    # Remove a value from a list
    def remove_from_list(self, list_name, value, provider = None):
        pkey = ""
        if provider is not None:
            pkey = "|" + provider
        main_list = self.get_list(list_name)
        try:
            self.table_service.delete_entity(self.table_name, list_name, value + pkey)
        except ValueError:
            pass
        else:
            main_list.remove(value)
        
        return main_list

    # Get a value from a K/V pair
    def get_value(self, key):
        retval = ""
        try:
            items = self.table_service.query_entities(self.table_name, filter="PartitionKey eq '" + key + "'")
        except ValueError:
            pass
        else:
            for item in items:
                retval = item.RowKey
                
        return retval

    # Set a value for a K/V pair
    def set_value(self, key, value):
        item = Entity()
        item.PartitionKey = key
        item.RowKey = value
        retval = False

        try:
            entries = self.table_service.query_entities(self.table_name, filter="PartitionKey eq '" + key + "'")
            old_value = "invalid"
            for entry in entries:
                old_value = entry.RowKey
            self.table_service.delete_entity(self.table_name, key, old_value)
            self.table_service.insert_entity(self.table_name, item)
        except ValueError:
            pass
        else:
            retval = True

        return retval

    # Delete all data and load in the default data set
    def data_load(self):
        data_set = {
            "required-modules": [
                "custom-vnet|azurerm",
                "custom-sg|azurerm",
                "custom-blob|azurerm",
                "custom-vpc|aws",
                "custom-sg|aws"
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
                "azurerm_subnet_network_security_group_association|azurerm",
                "aws_internet_gateway|aws",
                "aws_route|aws",
                "aws_route_table|aws",
                "aws_route_table_association|aws",
                "aws_subnet|aws",
                "aws_vpc|aws",
                "aws_security_group|aws",
            ],
            "prevent-deletion": [
                "true"
            ],
            "default-provider": [
                "azurerm"
            ],
            "mandatory-tags": [
                "Department",
                "Environment"
            ],
            "max-cost": [
                "15"
            ],
            "ddb-encryption": [
                "true"
            ],
            "no-star-access": [
                "true"
            ]
        }

        # delete all entries
        items = self.table_service.query_entities(self.table_name)
        for itm in items:
            self.table_service.delete_entity(self.table_name, itm.PartitionKey, itm.RowKey)

        # add all entries
        for category in data_set:
            for value in data_set[category]:
                item = Entity()
                item.PartitionKey = category
                item.RowKey = value
                self.table_service.insert_entity(self.table_name, item)

        return True
