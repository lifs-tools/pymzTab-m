# SpectraRef

Reference to a spectrum in a spectrum file, for example a fragmentation spectrum has been used to support the identification. If a separate spectrum file has been used for fragmentation spectrum, this MUST be reported in the metadata section as additional ms_runs. The reference must be in the format ms_run[1-n]:{SPECTRA_REF} where SPECTRA_REF MUST follow the format defined in 5.2 (including references to chromatograms where these are used to inform identification). Multiple spectra MUST be referenced using a “|” delimited list for the (rare) cases in which search engines have combined or aggregated multiple spectra in advance of the search to make identifications.  If a fragmentation spectrum has not been used, the value should indicate the ms_run to which is identification is mapped e.g. “ms_run[1]”. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ms_run** | [**MsRun**](MsRun.md) |  | 
**reference** | **str** | The (vendor-dependendent) reference string to the actual mass spectrum.  | 

## Example

```python
from openapi_client.models.spectra_ref import SpectraRef

# TODO update the JSON string below
json = "{}"
# create an instance of SpectraRef from a JSON string
spectra_ref_instance = SpectraRef.from_json(json)
# print the JSON string representation of the object
print(SpectraRef.to_json())

# convert the object into a dict
spectra_ref_dict = spectra_ref_instance.to_dict()
# create an instance of SpectraRef from a dict
spectra_ref_from_dict = SpectraRef.from_dict(spectra_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


