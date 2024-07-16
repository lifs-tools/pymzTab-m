# PublicationItem

A publication item, defined by a qualifier and a native accession, e.g. pubmed id.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type qualifier of this publication item. | [default to 'doi']
**accession** | **str** | The native accession id for this publication item. | 

## Example

```python
from openapi_client.models.publication_item import PublicationItem

# TODO update the JSON string below
json = "{}"
# create an instance of PublicationItem from a JSON string
publication_item_instance = PublicationItem.from_json(json)
# print the JSON string representation of the object
print(PublicationItem.to_json())

# convert the object into a dict
publication_item_dict = publication_item_instance.to_dict()
# create an instance of PublicationItem from a dict
publication_item_from_dict = PublicationItem.from_dict(publication_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


