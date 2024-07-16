# MsRun

Specification of ms_run.  location: Location of the external data file e.g. raw files on which analysis has been performed. If the actual location of the MS run is unknown, a “null” MUST be used as a place holder value, since the [1-n] cardinality is referenced elsewhere. If pre-fractionation has been performed, then [1-n] ms_runs SHOULD be created per assay.  instrument_ref: If different instruments are used in different runs, instrument_ref can be used to link a specific instrument to a specific run.  format: Parameter specifying the data format of the external MS data file. If ms_run[1-n]-format is present, ms_run[1-n]-id_format SHOULD also be present, following the parameters specified in Table 1.  id_format: Parameter specifying the id format used in the external data file. If ms_run[1-n]-id_format is present, ms_run[1-n]-format SHOULD also be present. fragmentation_method: The type(s) of fragmentation used in a given ms run. scan_polarity: The polarity mode of a given run. Usually only one value SHOULD be given here except for the case of mixed polarity runs. hash: Hash value of the corresponding external MS data file defined in ms_run[1-n]-location. If ms_run[1-n]-hash is present, ms_run[1-n]-hash_method SHOULD also be present. hash_method: A parameter specifying the hash methods used to generate the String in ms_run[1-n]-hash. Specifics of the hash method used MAY follow the definitions of the mzML format. If ms_run[1-n]-hash is present, ms_run[1-n]-hash_method SHOULD also be present. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** | The msRun&#39;s name. | [optional] 
**location** | **str** | The msRun&#39;s location URI. | 
**instrument_ref** | [**Instrument**](Instrument.md) |  | [optional] 
**format** | [**Parameter**](Parameter.md) |  | [optional] 
**id_format** | [**Parameter**](Parameter.md) |  | [optional] 
**fragmentation_method** | [**List[Parameter]**](Parameter.md) | The fragmentation methods applied during this msRun. | [optional] [default to []]
**scan_polarity** | [**List[Parameter]**](Parameter.md) | The scan polarity/polarities used during this msRun. | [optional] [default to []]
**hash** | **str** | The file hash value of this msRun&#39;s data file. | [optional] 
**hash_method** | [**Parameter**](Parameter.md) |  | [optional] 

## Example

```python
from openapi_client.models.ms_run import MsRun

# TODO update the JSON string below
json = "{}"
# create an instance of MsRun from a JSON string
ms_run_instance = MsRun.from_json(json)
# print the JSON string representation of the object
print(MsRun.to_json())

# convert the object into a dict
ms_run_dict = ms_run_instance.to_dict()
# create an instance of MsRun from a dict
ms_run_from_dict = MsRun.from_dict(ms_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


