# openapi_client.ConvertPlainApi

All URIs are relative to *https://apps.lifs-tools.org/mztabvalidator/rest/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_plain_mz_tab_file**](ConvertPlainApi.md#convert_plain_mz_tab_file) | **POST** /convertPlain | 


# **convert_plain_mz_tab_file**
> MzTab convert_plain_mz_tab_file(body)



Converts an mzTab file in tab separated format to XML or JSON representation. If this method returns an error code 422, the provided file did not pass validation. 

### Example


```python
import openapi_client
from openapi_client.models.mz_tab import MzTab
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
    api_instance = openapi_client.ConvertPlainApi(api_client)
    body = 'body_example' # str | mzTab file that should be converted.

    try:
        api_response = api_instance.convert_plain_mz_tab_file(body)
        print("The response of ConvertPlainApi->convert_plain_mz_tab_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConvertPlainApi->convert_plain_mz_tab_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| mzTab file that should be converted. | 

### Return type

[**MzTab**](MzTab.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: text/tab-separated-values

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversion Okay |  -  |
**415** | Unsupported content type |  -  |
**422** | Invalid input |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

