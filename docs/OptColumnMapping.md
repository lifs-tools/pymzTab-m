# OptColumnMapping

Additional columns can be added to the end of the small molecule table. These column headers MUST start with the prefix “opt_” followed by the {identifier} of the object they reference: assay, study variable, MS run or “global” (if the value relates to all replicates). Column names MUST only contain the following characters: ‘A’-‘Z’, ‘a’-‘z’, ‘0’-‘9’, ‘’, ‘-’, ‘[’, ‘]’, and ‘:’. CV parameter accessions MAY be used for optional columns following the format: opt{identifier}_cv_{accession}_\\{parameter name}. Spaces within the parameter’s name MUST be replaced by ‘_’. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The fully qualified column name. | 
**param** | [**Parameter**](Parameter.md) |  | [optional] 
**value** | **str** | The value for this column in a particular row. | [optional] 

## Example

```python
from openapi_client.models.opt_column_mapping import OptColumnMapping

# TODO update the JSON string below
json = "{}"
# create an instance of OptColumnMapping from a JSON string
opt_column_mapping_instance = OptColumnMapping.from_json(json)
# print the JSON string representation of the object
print(OptColumnMapping.to_json())

# convert the object into a dict
opt_column_mapping_dict = opt_column_mapping_instance.to_dict()
# create an instance of OptColumnMapping from a dict
opt_column_mapping_from_dict = OptColumnMapping.from_dict(opt_column_mapping_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


