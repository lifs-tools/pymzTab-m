# SampleProcessing

A list of parameters describing a sample processing, preparation or handling step similar to a biological or analytical methods report. The order of the sample_processing items should reflect the order these processing steps were performed in. If multiple parameters are given for a step these MUST be separated by a “|”. If derivatization was performed, it MUST be reported here as a general step, e.g. 'silylation' and the actual derivatization agens MUST be specified in the Section 6.2.54 part.       

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**sample_processing** | [**List[Parameter]**](Parameter.md) | Parameters specifiying sample processing that was applied within one step. | [optional] [default to []]

## Example

```python
from openapi_client.models.sample_processing import SampleProcessing

# TODO update the JSON string below
json = "{}"
# create an instance of SampleProcessing from a JSON string
sample_processing_instance = SampleProcessing.from_json(json)
# print the JSON string representation of the object
print(SampleProcessing.to_json())

# convert the object into a dict
sample_processing_dict = sample_processing_instance.to_dict()
# create an instance of SampleProcessing from a dict
sample_processing_from_dict = SampleProcessing.from_dict(sample_processing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


