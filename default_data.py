import configparser
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

# Start over
items = table_service.query_entities(table_name)
for itm in items:
    table_service.delete_entity(table_name, itm.PartitionKey, itm.RowKey)

# Add new entries
item = Entity()
item.PartitionKey = "required-modules"
item.RowKey = "custom-vnet"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "required-modules"
item.RowKey = "custom-sg"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "required-modules"
item.RowKey = "custom-blob"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "approved-instances"
item.RowKey = "Standard_A1_v2"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "approved-instances"
item.RowKey = "Standard_A2_v2"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "approved-instances"
item.RowKey = "Standard_A4_v2"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "approved-instances"
item.RowKey = "Standard_A8_v2"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "prohibited-resources"
item.RowKey = "azurerm_resource_group"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "prohibited-resources"
item.RowKey = "azurerm_virtual_network"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "prohibited-resources"
item.RowKey = "azurerm_network_security_group"
table_service.insert_entity('kevincx-cosmos-table', item)

item = Entity()
item.PartitionKey = "prohibited-resources"
item.RowKey = "azurerm_subnet_network_security_group_association"
table_service.insert_entity('kevincx-cosmos-table', item)
