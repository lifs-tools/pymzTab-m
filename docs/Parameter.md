# Parameter

mzTab makes use of CV parameters. As mzTab is expected to be used in several experimental environments where parameters might not yet be available for the generated scores etc. all parameters can either report CV parameters or user parameters that only contain a name and a value. Parameters are always reported as [CV label, accession, name, value]. Any field that is not available MUST be left empty. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**cv_label** | **str** |  | [optional] [default to '']
**cv_accession** | **str** |  | [optional] [default to '']
**name** | **str** |  | 
**value** | **str** |  | [default to '']

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


