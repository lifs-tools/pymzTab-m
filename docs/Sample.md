# Sample

Specification of sample. (empty) name: A name for each sample to serve as a list of the samples that MUST be reported in the following tables. Samples MUST be reported if a statistical design is being captured (i.e. bio or tech replicates). If the type of replicates are not known, samples SHOULD NOT be reported.  species: The respective species of the samples analysed. For more complex cases, such as metagenomics, optional columns and userParams should be used.  tissue: The respective tissue(s) of the sample.  cell_type: The respective cell type(s) of the sample.  disease: The respective disease(s) of the sample.  description: A human readable description of the sample.  custom: Custom parameters describing the sample's additional properties. Dates MUST be provided in ISO-8601 format. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** | The sample&#39;s name. | [optional] 
**custom** | [**List[Parameter]**](Parameter.md) | Additional user or cv parameters. | [optional] [default to []]
**species** | [**List[Parameter]**](Parameter.md) | Biological species information on the sample. | [optional] [default to []]
**tissue** | [**List[Parameter]**](Parameter.md) | Biological tissue information on the sample. | [optional] [default to []]
**cell_type** | [**List[Parameter]**](Parameter.md) | Biological cell type information on the sample. | [optional] [default to []]
**disease** | [**List[Parameter]**](Parameter.md) | Disease information on the sample. | [optional] [default to []]
**description** | **str** | A free form description of the sample. | [optional] 

## Example

```python
from openapi_client.models.sample import Sample

# TODO update the JSON string below
json = "{}"
# create an instance of Sample from a JSON string
sample_instance = Sample.from_json(json)
# print the JSON string representation of the object
print(Sample.to_json())

# convert the object into a dict
sample_dict = sample_instance.to_dict()
# create an instance of Sample from a dict
sample_from_dict = Sample.from_dict(sample_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


