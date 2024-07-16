# Instrument

The name, source, analyzer and detector of the instruments used in the experiment. Multiple instruments are numbered [1-n].

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | [**Parameter**](Parameter.md) |  | [optional] 
**source** | [**Parameter**](Parameter.md) |  | [optional] 
**analyzer** | [**List[Parameter]**](Parameter.md) | The instrument&#39;s mass analyzer, as defined by the parameter. | [optional] [default to []]
**detector** | [**Parameter**](Parameter.md) |  | [optional] 

## Example

```python
from openapi_client.models.instrument import Instrument

# TODO update the JSON string below
json = "{}"
# create an instance of Instrument from a JSON string
instrument_instance = Instrument.from_json(json)
# print the JSON string representation of the object
print(Instrument.to_json())

# convert the object into a dict
instrument_dict = instrument_instance.to_dict()
# create an instance of Instrument from a dict
instrument_from_dict = Instrument.from_dict(instrument_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


