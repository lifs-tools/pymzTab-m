# ColumnParameterMapping

Defines the used unit for a column in the mzTab-M file. The format of the value has to be \\{column name}=\\{Parameter defining the unit}. This field MUST NOT be used to define a unit for quantification columns. The unit used for small molecule quantification values MUST be set in small_molecule-quantification_unit.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** | The fully qualified target column name. | 
**param** | [**Parameter**](Parameter.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


