# Database

Specification of databases. (empty): The description of databases used. For cases, where a known database has not been used for identification, a userParam SHOULD be inserted to describe any identification performed e.g. de novo. If no identification has been performed at all then \"no database\" should be inserted followed by null. prefix: The prefix used in the “identifier” column of data tables. For the “no database” case \"null\" must be used. version: The database version is mandatory where identification has been performed. This may be a formal version number e.g. “1.4.1”, a date of access “2016-10-27” (ISO-8601 format) or “Unknown” if there is no suitable version that can be annotated. uri: The URI to the database. For the “no database” case, \"null\" must be reported. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**param** | [**Parameter**](Parameter.md) |  | 
**prefix** | **str** | The database prefix. | [default to 'null']
**version** | **str** | The database version. | 
**uri** | **str** | The URI to the online database. | 

## Example

```python
from openapi_client.models.database import Database

# TODO update the JSON string below
json = "{}"
# create an instance of Database from a JSON string
database_instance = Database.from_json(json)
# print the JSON string representation of the object
print(Database.to_json())

# convert the object into a dict
database_dict = database_instance.to_dict()
# create an instance of Database from a dict
database_from_dict = Database.from_dict(database_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


