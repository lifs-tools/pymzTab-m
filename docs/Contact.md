# Contact

The contact’s name, affiliation and e-mail. Several contacts can be given by indicating the number in the square brackets after \"contact\". A contact has to be supplied in the format [first name] [initials] [last name]. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** | The contact&#39;s name. | [optional] 
**affiliation** | **str** | The contact&#39;s affiliation. | [optional] 
**email** | **str** | The contact&#39;s e-mail address. | [optional] 
**orcid** | **str** | The contact&#39;s orcid id, without https prefix. | [optional] 

## Example

```python
from openapi_client.models.contact import Contact

# TODO update the JSON string below
json = "{}"
# create an instance of Contact from a JSON string
contact_instance = Contact.from_json(json)
# print the JSON string representation of the object
print(Contact.to_json())

# convert the object into a dict
contact_dict = contact_instance.to_dict()
# create an instance of Contact from a dict
contact_from_dict = Contact.from_dict(contact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


