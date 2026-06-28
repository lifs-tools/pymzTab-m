# PublicationItem

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
custom|List of <code>ExtendedParameter</code>|-|Additional parameters for the field, separated by bars\.
type|<code>str</code>|pattern: <code>doi\|pubmed\|uri</code><br/>Validation type: **<code>error</code>**|The type qualifier of this publication item\.
accession|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The native accession id for this publication item\.
