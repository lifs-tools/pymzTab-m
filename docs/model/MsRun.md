# MsRun

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
custom|List of <code>ExtendedParameter</code>|-|Additional parameters for the field, separated by bars\.
id|<code>int</code>|-|
name|<code>str</code>|-|The msRun's name\.
location|<code>str</code>|**required**<br/>format: <code>any-url</code><br/>Validation type: **<code>error</code>**|The msRun's location URI\.
instrument_ref|<code>int</code>|-|Sample reference\.
format|<code>Parameter</code>|-|The format of the MS run file\.
id_format|<code>Parameter</code>|-|The format of the IDs in the MS run file\.
fragmentation_method|List of <code>Parameter</code>|-|The fragmentation methods applied during this msRun\.
scan_polarity|List of <code>Parameter</code>|-|The scan polarity/polarities used during this msRun\.
hash|<code>str</code>|-|The file hash value of this msRun's data file\.
hash_method|<code>Parameter</code>|-|The method used to calculate the hash\.
