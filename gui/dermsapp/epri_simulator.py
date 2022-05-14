# constants for EPRI remote on 18.216.194.249:8080 bindings
# BASE_URL = "http://18.216.194.249:8080"       # old url
BASE_URL = "http://3.142.173.151:8080"          # current url
CREATE_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/create/executeDERGroups?wsdl"
CHANGE_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/change/executeDERGroups?wsdl"
CREATE_NAMESPACE_SOAP_BINDING = (
        '{http://create.ws.server.sixthc.com/}ExecuteDERGroupsServiceSoapBinding',
        f'{BASE_URL}/61968-5/create/executeDERGroups'
)
CHANGE_NAMESPACE_SOAP_BINDING = (
        '{http://change.ws.server.sixthc.com/}ExecuteDERGroupsServiceSoapBinding',
        f'{BASE_URL}/61968-5/change/executeDERGroups'
)
QUERY_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/get/queryDERGroups?wsdl"
QUERY_NAMESPACE_SOAP_BINDING = (
        '{http://get.ws.server.sixthc.com/}QueryDERGroupsServiceSoapBinding',
        f'{BASE_URL}/61968-5/get/queryDERGroups'
)
QUERY_DERGROUP_STATUS_ENDPOINT = f"{BASE_URL}/61968-5/get/queryDERGroupStatuses?wsdl"
QUERY_NAMESPACE_STATUS_SOAP_BINDING = (
        '{http://get.ws.server.sixthc.com/}QueryDERGroupStatusesServiceSoapBinding',
        f'{BASE_URL}/61968-5/get/queryDERGroupStatuses'
)

CREATE_DISPATCH_ENDPOINT = f"{BASE_URL}/61968-5/create/executeDERGroupDispatches?wsdl"
CREATE_DISPATCH_NAMESPACE_SOAP_BINDING = (
        '{http://create.ws.server.sixthc.com/}ExecuteDERGroupDispatchesServiceSoapBinding',
        f'{BASE_URL}/61968-5/create/executeDERGroupDispatches'
)

QUERY_DERGROUP_FORECAST_ENDPOINT = f"{BASE_URL}/61968-5/get/queryDERGroupForecasts?wsdl"
QUERY_NAMESPACE_FORECAST_SOAP_BINDING = (
        '{http://get.ws.server.sixthc.com/}QueryDERGroupForecastsServiceSoapBinding',
        f'{BASE_URL}/61968-5/get/queryDERGroupForecasts'
)
