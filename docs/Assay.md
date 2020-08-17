# Assay

Specification of assay. (empty) name: A name for each assay, to serve as a list of the assays that MUST be reported in the following tables.  custom: Additional custom parameters or values for a given assay.  external_uri: An external reference uri to further information about the assay, for example via a reference to an object within an ISA-TAB file.  sample_ref: An association from a given assay to the sample analysed.  ms_run_ref: An association from a given assay to the source MS run. All assays MUST reference exactly one ms_run unless a workflow with pre-fractionation is being encoded, in which case each assay MUST reference n ms_runs where n fractions have been collected. Multiple assays SHOULD reference the same ms_run to capture multiplexed experimental designs. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** | The assay name. | 
**custom** | [**list[Parameter]**](Parameter.md) | Additional user or cv parameters. | [optional] 
**external_uri** | **str** | An external URI to further information about this assay. | [optional] 
**sample_ref** | [**Sample**](Sample.md) |  | [optional] 
**ms_run_ref** | [**list[MsRun]**](MsRun.md) | The ms run(s) referenced by this assay. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


