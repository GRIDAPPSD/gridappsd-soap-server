from SPARQLWrapper import SPARQLWrapper2

# URL from outside the docker container:
blazegraph_url = "http://localhost:8889/bigdata/sparql"

cim100 = '<http://iec.ch/TC57/CIM100#'
# Prefix for all queries.
prefix = """PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: {cimURL}>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
""".format(cimURL=cim100)


def insertEndDeviceGroup(endDeviceGroup):

    sparql = SPARQLWrapper2(blazegraph_url)

    q = (prefix + 'INSERT DATA { ')
    mRIDStr = str(endDeviceGroup.mRID)
    # Need an underscore on the ID.
    if mRIDStr[0] != '_':
        mRIDStr = '_' + mRIDStr

    group = '<' + blazegraph_url + '#' + mRIDStr + '>'

    q += group + ' a c:EndDeviceGroup .' + group + ' c:IdentifiedObject.mRID \"' + mRIDStr + '\" . ' + group + ' c:IdentifiedObject.name \"' + endDeviceGroup.description + '\" . '

    for device in endDeviceGroup.EndDevices:
        deviceID = str(device.mRID)
        if deviceID[0] != '_':
            deviceID = '_' + deviceID
        q += group + ' c:EndDevice \"' + deviceID + '\" .'

    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    sparql.method = 'POST'
    ret = sparql.query()
    print(ret)