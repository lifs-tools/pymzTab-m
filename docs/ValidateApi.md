# mztab_m_swagger_client.ValidateApi

All URIs are relative to *https://apps.lifs.isas.de/mztabvalidator/rest/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**validate_mz_tab_file**](ValidateApi.md#validate_mz_tab_file) | **POST** /validate | 


# **validate_mz_tab_file**
> list[ValidationMessage] validate_mz_tab_file(mztabfile, level=level, max_errors=max_errors, semantic_validation=semantic_validation)



Validates an mzTab file in XML or JSON representation and reports syntactic, structural, and semantic errors. 

### Example

```python
from __future__ import print_function
import time
import mztab_m_swagger_client
from mztab_m_swagger_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with mztab_m_swagger_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = mztab_m_swagger_client.ValidateApi(api_client)
    mztabfile = mztab_m_swagger_client.MzTab() # MzTab | mzTab file that should be validated.
level = 'info' # str | The level of errors that should be reported, one of ERROR, WARN, INFO. (optional) (default to 'info')
max_errors = 100 # int | The maximum number of errors to return. (optional) (default to 100)
semantic_validation = False # bool | Whether a semantic validation against the default rule set should be performed. (optional) (default to False)

    try:
        api_response = api_instance.validate_mz_tab_file(mztabfile, level=level, max_errors=max_errors, semantic_validation=semantic_validation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ValidateApi->validate_mz_tab_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mztabfile** | [**MzTab**](MzTab.md)| mzTab file that should be validated. | 
 **level** | **str**| The level of errors that should be reported, one of ERROR, WARN, INFO. | [optional] [default to &#39;info&#39;]
 **max_errors** | **int**| The maximum number of errors to return. | [optional] [default to 100]
 **semantic_validation** | **bool**| Whether a semantic validation against the default rule set should be performed. | [optional] [default to False]

### Return type

[**list[ValidationMessage]**](ValidationMessage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Validation Okay |  -  |
**415** | Unsupported content type |  -  |
**422** | Invalid input |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

