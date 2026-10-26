# OptColumnMapping

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
identifier|<code>Parameter</code>|**required**<br/>pattern: <code>^global\|ms\_run\\\[\\d\+\\\]\|assay\\\[\\d\+\\\]\|study\_variable\\\[\\d\+\\\]</code><br/>Validation type: **<code>error</code>**|The fully qualified column name\.
param|<code>Parameter</code>|**required**<br/>Validation type: **<code>error</code>**|The fully qualified column parameter\.
value|<code>str</code>|-|The value for this column in a particular row\.
