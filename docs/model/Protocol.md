# Protocol

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
id|<code>int</code>|-|
name|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The protocol name\.
type|<code>Parameter</code>|**required**<br/>Validation type: **<code>error</code>**|The protocol type, as defined by the parameter\.
description|<code>str</code>|-|Description of the protocol\.
parameter|List of <code>ExtendedParameter</code>|-|The protocol parameters\.
