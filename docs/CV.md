# CV

Specification of controlled vocabularies. label: A string describing the labels of the controlled vocabularies/ontologies used in the mzTab file as a short-hand e.g. \"MS\" for PSI-MS. full_name: A string describing the full names of the controlled vocabularies/ontologies used in the mzTab file. version: A string describing the version of the controlled vocabularies/ontologies used in the mzTab file. uri: A string containing the URIs of the controlled vocabularies/ontologies used in the mzTab file. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**label** | **str** | The abbreviated CV label. | 
**full_name** | **str** | The full name of this CV, for humans. | 
**version** | **str** | The CV version used when the file was generated. | 
**uri** | **str** | A URI to the CV definition. | 

## Example

```python
from openapi_client.models.cv import CV

# TODO update the JSON string below
json = "{}"
# create an instance of CV from a JSON string
cv_instance = CV.from_json(json)
# print the JSON string representation of the object
print(CV.to_json())

# convert the object into a dict
cv_dict = cv_instance.to_dict()
# create an instance of CV from a dict
cv_from_dict = CV.from_dict(cv_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


