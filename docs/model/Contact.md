# Contact

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
custom|List of <code>ExtendedParameter</code>|-|Additional parameters for the field, separated by bars\.
id|<code>int</code>|-|
name|<code>str</code>|-|The contact's name\.
affiliation|<code>str</code>|-|The contact's affiliation\.
email|<code>str</code>|format: <code>email</code><br/>Validation type: **<code>error</code>**|The contact's e\-mail address\.
orcid|<code>str</code>|pattern: <code>^\[0\-9\]\{4\}\-\[0\-9\]\{4\}\-\[0\-9\]\{4\}\-\[0\-9\]\{3\}\[0\-9X\]\{1\}$</code><br/>Validation type: **<code>error</code>**|The contact's orcid id, without https prefix\.
