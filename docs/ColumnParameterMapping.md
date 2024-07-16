# ColumnParameterMapping

Defines the used unit for a column in the mzTab-M file. The format of the value has to be \\{column name}=\\{Parameter defining the unit}. This field MUST NOT be used to define a unit for quantification columns. The unit used for small molecule quantification values MUST be set in small_molecule-quantification_unit.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** | The fully qualified target column name. | 
**param** | [**Parameter**](Parameter.md) |  | 

## Example

```python
from openapi_client.models.column_parameter_mapping import ColumnParameterMapping

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnParameterMapping from a JSON string
column_parameter_mapping_instance = ColumnParameterMapping.from_json(json)
# print the JSON string representation of the object
print(ColumnParameterMapping.to_json())

# convert the object into a dict
column_parameter_mapping_dict = column_parameter_mapping_instance.to_dict()
# create an instance of ColumnParameterMapping from a dict
column_parameter_mapping_from_dict = ColumnParameterMapping.from_dict(column_parameter_mapping_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


