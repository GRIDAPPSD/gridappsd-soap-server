"""
Created on Apr 24, 2018

@author: thay838
@author: craig8
"""
# ******************************************************************************
# URL for blazegraph

# Using the default blazegraph installation as a standalone
# blazegraph_url = "http://localhost:9999/blazegraph/namespace/kb/sparql"

# When running the platform in the docker, the blazegraph URL can be found in
# /gridappsd/conf/pnnl.goss.gridappsd.cfg. At the time of writing (04/24/18),
# there are two URLs. One for calling from inside the docker container, and one
# for calling from outside the docker container.

# depends on what we are testing, choose locate gridappsD binding or remote binding
USE_SIMULATOR_FOR_SOAP = None

# if USE_SIMULATOR_FOR_SOAP:
#     from .epri_simulator import (CREATE_NAMESPACE_SOAP_BINDING, CHANGE_NAMESPACE_SOAP_BINDING,
#                                  CREATE_DERGROUP_ENDPOINT, CHANGE_DERGROUP_ENDPOINT, QUERY_DERGROUP_ENDPOINT,
#                                  QUERY_NAMESPACE_SOAP_BINDING)
# else:
from epri_opendss import (CREATE_NAMESPACE_SOAP_BINDING, CHANGE_NAMESPACE_SOAP_BINDING,
                           CREATE_DERGROUP_ENDPOINT, CHANGE_DERGROUP_ENDPOINT, GET_DEVICE_ENDPOINT,
                           GET_DERGROUPS_ENDPOINT, QUERY_DERGROUP_ENDPOINT, QUERY_NAMESPACE_SOAP_BINDING,
                           QUERY_DERGROUP_STATUS_ENDPOINT, QUERY_NAMESPACE_STATUS_SOAP_BINDING,
                           QUERY_DERGROUP_FORECAST_ENDPOINT, QUERY_NAMESPACE_FORECAST_SOAP_BINDING,
                           GET_MODEL_ENDPOINT, CHANGE_SIMULATION_ENDPOINT,
                           CREATE_DISPATCH_ENDPOINT, CREATE_DISPATCH_NAMESPACE_SOAP_BINDING)


def re_import():
    import sys
    print(sys.modules)
    if USE_SIMULATOR_FOR_SOAP:
        from importlib import reload
        from .epri_simulator import (CREATE_NAMESPACE_SOAP_BINDING, CHANGE_NAMESPACE_SOAP_BINDING,
                                      CREATE_DERGROUP_ENDPOINT, CHANGE_DERGROUP_ENDPOINT,
                                      QUERY_DERGROUP_ENDPOINT, QUERY_NAMESPACE_SOAP_BINDING,
                                     QUERY_NAMESPACE_STATUS_SOAP_BINDING, QUERY_DERGROUP_STATUS_ENDPOINT,
                                     CREATE_DISPATCH_ENDPOINT, CREATE_DISPATCH_NAMESPACE_SOAP_BINDING,
                                     QUERY_DERGROUP_FORECAST_ENDPOINT, QUERY_NAMESPACE_FORECAST_SOAP_BINDING)
        print(CREATE_NAMESPACE_SOAP_BINDING)



# URL from inside the docker container:
# blazegraph_url = "http://blazegraph:8080/bigdata/sparql"

# URL from outside the docker container:
blazegraph_url = "http://localhost:8889/bigdata/namespace/kb/sparql"
#
# # ******************************************************************************
# # URL for derms test instance
# BASE_URL = "http://172.20.10.6:9000"
# # BASE_URL = "http://18.216.194.249:8080"
# # CREATE_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/create/executeDERGroups?wsdl"
# CREATE_DERGROUP_ENDPOINT = f"{BASE_URL}/service/org/epri/dergroups/create?wsdl"
# CREATE_NAMESPACE_SOAP_BINDING = (
#         '{http://iec.ch/TC57/2017/ExecuteDERGroups}ExecuteDERGroupsSoapBinding',
#         'http://172.20.10.6:9000/service/org/epri/dergroups/create'
# )
#
# # CHANGE_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/change/executeDERGroups?wsdl"
# CHANGE_DERGROUP_ENDPOINT = f"{BASE_URL}/service/org/epri/dergroups/change?wsdl"
# CHANGE_NAMESPACE_SOAP_BINDING = (
#     '{http://iec.ch/TC57/2017/ExecuteDERGroups}ExecuteDERGroupsSoapBinding',
#     'http://172.20.10.6:9000/service/org/epri/dergroups/change'
# )
# # http://18.216.194.249:8080/61968-5/change/receiveDERGroups?wsdl"
# DISPATCH_DERGROUP_ENDPOINT = f"{BASE_URL}/61968-5/create/executeDERGroupDispatches?wsdl"


SOAP_BINDINGS = dict(
    CREATE=CREATE_NAMESPACE_SOAP_BINDING,
    # Both delete and change use the same binding
    DELETE=CHANGE_NAMESPACE_SOAP_BINDING,
    CHANGE=CHANGE_NAMESPACE_SOAP_BINDING,
    GET=QUERY_NAMESPACE_SOAP_BINDING
)
STATUS_SOAP_BINDINGS = dict(
    CREATE=CREATE_NAMESPACE_SOAP_BINDING,
    # Both delete and change use the same binding
    DELETE=CHANGE_NAMESPACE_SOAP_BINDING,
    CHANGE=CHANGE_NAMESPACE_SOAP_BINDING,
    GET=QUERY_NAMESPACE_STATUS_SOAP_BINDING
)

SOAP_BINDINGS_DISPATCH = dict(
    CREATE=CREATE_DISPATCH_NAMESPACE_SOAP_BINDING
)
FORECASTS_SOAP_BINDINGS = dict(
    CREATE=CREATE_NAMESPACE_SOAP_BINDING,
    # Both delete and change use the same binding
    DELETE=CHANGE_NAMESPACE_SOAP_BINDING,
    CHANGE=CHANGE_NAMESPACE_SOAP_BINDING,
    GET=QUERY_NAMESPACE_FORECAST_SOAP_BINDING
)

# ******************************************************************************
# Prefix for blazegraph queries; canonical version is now CIM100

cim100 = '<http://iec.ch/TC57/CIM100#'
# Prefix for all queries.
prefix = """PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: {cimURL}>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
""".format(cimURL=cim100)

# cim17 is used in InsertMeasurements.py prior to summer 2019. 
# Notice the lack of "greater than" at the end.
cim17 = '<http://iec.ch/TC57/2012/CIM-schema-cim17#'
# Prefix for all queries.
prefix17 = """PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: {cimURL}>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
""".format(cimURL=cim17)
#******************************************************************************

# cim16 is used for some utility feeders and ListOverheadWires.py, ListCNCables.py
cim16 = '<http://iec.ch/TC57/2012/CIM-schema-cim16#'
# Prefix for all queries.
prefix16 = """PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: {cimURL}>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
""".format(cimURL=cim16)
#******************************************************************************


