# StudyVariable

## Properties

|Name (Alias)|Type (Default)|Constraints|Description|
|---|---|----|----------|
custom|List of <code>ExtendedParameter</code>|-|Additional parameters for the field, separated by bars\.
id|<code>int</code>|-|
name|<code>str</code>|**required**<br/>Validation type: **<code>error</code>**|The study variable name\.
group_refs|List of <code>int</code>|format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|The study variable group this study variable belongs to\.
assay_refs|List of <code>int</code>|format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|The assays referenced by this study variable\.
ms_run_refs|List of <code>int</code>|format: <code>non-negative-integer</code><br/>Validation type: **<code>error</code>**|The ms run\(s\) referenced by this study variable\.
average_function|<code>Parameter</code>|-|The function used to calculate the study variable quantification value and the operation used is not arithmetic mean \(default\)\. e\.g\. geometric mean, median\.
variation_function|<code>Parameter</code>|-|The function used to calculate the study variable quantification variation value if it is reported and the operation used is not coefficient of variation \(default\)\. e\.g\. standard error\.
description|<code>str</code>|-|A free\-form description of this study variable\.
