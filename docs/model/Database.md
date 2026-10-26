# Database

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
id|<code>int</code>|-|
param|<code>Parameter</code>|**required**<br/>Validation type: **<code>error</code>**|The database name\.
prefix|<code>str</code>|**required**<br/>Validation type: **<code>warn</code>**|The prefix used in the “identifier” column of data tables\. For the 'no database' case 'null' must be used\.
version|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The database version is mandatory where identification has been performed\. This may be a formal version number e\.g\. “1\.4\.1”, a date of access “2016\-10\-27” \(ISO\-8601 format\) or “Unknown” if there is no suitable version that can be annotated\.
uri|<code>str</code>|**required**<br/>Validation type: **<code>warn</code>**|The URI to the database\. For the “no database” case, 'null' must be reported\.
