# openapi_client.ConvertApi

All URIs are relative to *https://apps.lifs-tools.org/mztabvalidator/rest/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_mz_tab_file**](ConvertApi.md#convert_mz_tab_file) | **POST** /convert | 


# **convert_mz_tab_file**
> str convert_mz_tab_file(mz_tab)



Converts an mzTab file in JSON or XML format to the tab-separated representation. If this method returns an error code 422, the provided file did not pass validation. 

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
    api_instance = openapi_client.ConvertApi(api_client)
    mz_tab = openapi_client.MzTab() # MzTab | mzTab file that should be validated.

    try:
        api_response = api_instance.convert_mz_tab_file(mz_tab)
        print("The response of ConvertApi->convert_mz_tab_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConvertApi->convert_mz_tab_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mz_tab** | [**MzTab**](MzTab.md)| mzTab file that should be validated. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/tab-separated-values, text/plain
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversion Okay |  -  |
**415** | Unsupported content type |  -  |
**422** | Invalid input |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

