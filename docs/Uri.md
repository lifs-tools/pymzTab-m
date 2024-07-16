# Uri

A URI pointing to the file’s source data (e.g., a MetaboLights records) or an external file with more details about the study design.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**value** | **str** | The URI pointing to the external resource. | [optional] 

## Example

```python
from openapi_client.models.uri import Uri

# TODO update the JSON string below
json = "{}"
# create an instance of Uri from a JSON string
uri_instance = Uri.from_json(json)
# print the JSON string representation of the object
print(Uri.to_json())

# convert the object into a dict
uri_dict = uri_instance.to_dict()
# create an instance of Uri from a dict
uri_from_dict = Uri.from_dict(uri_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


