# openapi_client.ValidatePlainApi

All URIs are relative to *https://apps.lifs-tools.org/mztabvalidator/rest/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**validate_plain_mz_tab_file**](ValidatePlainApi.md#validate_plain_mz_tab_file) | **POST** /validatePlain | 


# **validate_plain_mz_tab_file**
> List[ValidationMessage] validate_plain_mz_tab_file(body, level=level, max_errors=max_errors, semantic_validation=semantic_validation)



Validates an mzTab file in plain text representation / tab-separated format and reports syntactic, structural, and semantic errors. 

### Example


```python
import openapi_client
from openapi_client.models.validation_message import ValidationMessage
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://apps.lifs-tools.org/mztabvalidator/rest/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://apps.lifs-tools.org/mztabvalidator/rest/v2"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ValidatePlainApi(api_client)
    body = 'body_example' # str | mzTab file that should be validated.
    level = info # str | The level of errors that should be reported, one of ERROR, WARN, INFO. (optional) (default to info)
    max_errors = 100 # int | The maximum number of errors to return. (optional) (default to 100)
    semantic_validation = False # bool | Whether a semantic validation against the default rule set should be performed. (optional) (default to False)

    try:
        api_response = api_instance.validate_plain_mz_tab_file(body, level=level, max_errors=max_errors, semantic_validation=semantic_validation)
        print("The response of ValidatePlainApi->validate_plain_mz_tab_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ValidatePlainApi->validate_plain_mz_tab_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| mzTab file that should be validated. | 
 **level** | **str**| The level of errors that should be reported, one of ERROR, WARN, INFO. | [optional] [default to info]
 **max_errors** | **int**| The maximum number of errors to return. | [optional] [default to 100]
 **semantic_validation** | **bool**| Whether a semantic validation against the default rule set should be performed. | [optional] [default to False]

### Return type

[**List[ValidationMessage]**](ValidationMessage.md)

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

