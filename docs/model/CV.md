# CV

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
custom|List of <code>ExtendedParameter</code>|-|Additional parameters for the field, separated by bars\.
id|<code>int</code>|-|
label|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The abbreviated CV label\.
full_name|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The full name of this CV, for humans\.
version|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The CV version used when the file was generated\.
uri|<code>str</code>|**required**<br/>format: <code>any-url</code><br/>Validation type: **<code>error</code>**|A URI to the CV definition\.
