# Software

Software used to analyze the data and obtain the reported results. The parameter’s value SHOULD contain the software’s version. The order (numbering) should reflect the order in which the tools were used. A software setting used. This field MAY occur multiple times for a single software. The value of this field is deliberately set as a String, since there currently do not exist CV terms for every possible setting. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**parameter** | [**Parameter**](Parameter.md) |  | [optional] 
**setting** | **list[str]** | A software setting used. This field MAY occur multiple times for a single software. The value of this field is deliberately set as a String, since there currently do not exist cvParams for every possible setting.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


