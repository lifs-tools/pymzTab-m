# openapi_client.ValidatePlainApi

All URIs are relative to *https://apps.lifs.isas.de/mztabvalidator/rest/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**validate_plain_mz_tab_file**](ValidatePlainApi.md#validate_plain_mz_tab_file) | **POST** /validatePlain | 


# **validate_plain_mz_tab_file**
> list[ValidationMessage] validate_plain_mz_tab_file(mztabfile, level=level, max_errors=max_errors, semantic_validation=semantic_validation)



Validates an mzTab file in plain text representation / tab-separated format and reports syntactic, structural, and semantic errors. 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ValidatePlainApi(api_client)
    mztabfile = 'mztabfile_example' # str | mzTab file that should be validated.
level = 'info' # str | The level of errors that should be reported, one of ERROR, WARN, INFO. (optional) (default to 'info')
max_errors = 100 # int | The maximum number of errors to return. (optional) (default to 100)
semantic_validation = False # bool | Whether a semantic validation against the default rule set should be performed. (optional) (default to False)

    try:
        api_response = api_instance.validate_plain_mz_tab_file(mztabfile, level=level, max_errors=max_errors, semantic_validation=semantic_validation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ValidatePlainApi->validate_plain_mz_tab_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mztabfile** | **str**| mzTab file that should be validated. | 
 **level** | **str**| The level of errors that should be reported, one of ERROR, WARN, INFO. | [optional] [default to &#39;info&#39;]
 **max_errors** | **int**| The maximum number of errors to return. | [optional] [default to 100]
 **semantic_validation** | **bool**| Whether a semantic validation against the default rule set should be performed. | [optional] [default to False]

### Return type

[**list[ValidationMessage]**](ValidationMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/tab-separated-values, text/plain
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Validation Okay |  -  |
**415** | Unsupported content type |  -  |
**422** | Invalid input |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

