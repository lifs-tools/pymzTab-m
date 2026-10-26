# Assay

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
id|<code>int</code>|-|
name|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The assay name\.
custom|List of <code>Parameter</code>|-|Additional user or cv parameters\.
external_uri|<code>str</code>|format: <code>any-url</code><br/>Validation type: **<code>error</code>**|An external URI to further information about this assay\.
sample_ref|<code>int</code>|-|Sample reference\.
ms_run_refs<br/>(ms_run_ref)|List of <code>int</code>|**required**<br/>min: 1<br/>format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|The ms run\(s\) referenced by this assay\.
protocol_refs|List of <code>int</code>|format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|The protocol\(s\) referenced by this assay\.
parameters|List of <code>ExtendedParameter</code>|-|Additional parameters of the assay, separated by bars\.
