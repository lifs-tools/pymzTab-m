# Publication

A publication associated with this file. Several publications can be given by indicating the number in the square brackets after “publication”. PubMed ids must be prefixed by “pubmed:”, DOIs by “doi:”. Multiple identifiers MUST be separated by “|”. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**publication_items** | [**List[PublicationItem]**](PublicationItem.md) | The publication item ids referenced by this publication. | [default to []]

## Example

```python
from openapi_client.models.publication import Publication

# TODO update the JSON string below
json = "{}"
# create an instance of Publication from a JSON string
publication_instance = Publication.from_json(json)
# print the JSON string representation of the object
print(Publication.to_json())

# convert the object into a dict
publication_dict = publication_instance.to_dict()
# create an instance of Publication from a dict
publication_from_dict = Publication.from_dict(publication_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


