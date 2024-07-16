# StudyVariable

Specification of study_variable. (empty) name: A name for each study variable (experimental condition or factor), to serve as a list of the study variables that MUST be reported in the following tables. For software that does not capture study variables, a single study variable MUST be reported, linking to all assays. This single study variable MUST have the identifier “undefined“. assay_refs: Bar-separated references to the IDs of assays grouped in the study variable. average_function: The function used to calculate the study variable quantification value and the operation used is not arithmetic mean (default) e.g. “geometric mean”, “median”. The 1-n refers to different study variables. variation_function: The function used to calculate the study variable quantification variation value if it is reported and the operation used is not coefficient of variation (default) e.g. “standard error”. description: A textual description of the study variable. factors: Additional parameters or factors, separated by bars, that are known about study variables allowing the capture of more complex, such as nested designs.   

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** | The study variable name. | 
**assay_refs** | [**List[Assay]**](Assay.md) | The assays referenced by this study variable. | [optional] [default to []]
**average_function** | [**Parameter**](Parameter.md) |  | [optional] 
**variation_function** | [**Parameter**](Parameter.md) |  | [optional] 
**description** | **str** | A free-form description of this study variable. | [optional] 
**factors** | [**List[Parameter]**](Parameter.md) | Parameters indicating which factors were used for the assays referenced by this study variable, and at which levels. | [optional] [default to []]

## Example

```python
from openapi_client.models.study_variable import StudyVariable

# TODO update the JSON string below
json = "{}"
# create an instance of StudyVariable from a JSON string
study_variable_instance = StudyVariable.from_json(json)
# print the JSON string representation of the object
print(StudyVariable.to_json())

# convert the object into a dict
study_variable_dict = study_variable_instance.to_dict()
# create an instance of StudyVariable from a dict
study_variable_from_dict = StudyVariable.from_dict(study_variable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


