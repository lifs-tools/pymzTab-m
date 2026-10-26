# Comment

Comment lines can be placed anywhere in an mzTab file.
These lines must start with the three-letter code COM
and are ignored by most parsers.
Empty lines can also occur anywhere in an mzTab file and are ignored.

## Example

<code>COM	This is a comment</code>

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
prefix|<code><code>str</code></code> (<code>COM</code>)|**required**<br/>pattern: <code>COM</code><br/>Validation type: **<code>error</code>**|Comment prefix
msg|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|message
line_number|<code>int</code>|format: <code>positive-integer</code><br/>Validation type: **<code>error</code>**|line number
