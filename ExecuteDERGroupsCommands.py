import uuid

from SPARQLWrapper import SPARQLWrapper2

# URL from outside the docker container:
from exceptions import SamemRIDException, SameGroupNameException

blazegraph_url = "http://localhost:8889/bigdata/sparql"

cim100 = '<http://iec.ch/TC57/CIM100#'
# Prefix for all queries.
prefix = """PREFIX r:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:{cimURL}>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
""".format(cimURL=cim100)

sparql = SPARQLWrapper2(blazegraph_url)

def checkmRIDExists(mrid):

    q = (prefix + 'Select ?id Where{ ' +
         '?id c:IdentifiedObject.mRID \"' + mrid + '\" . ')
    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    ret = sparql.query()
    print(ret)
    if ret.bindings:
        raise SamemRIDException


def checkNameExists(name):

    q = (prefix + 'Select ?id Where{ ' +
         '?id c:IdentifiedObject.name \"' + name + '\" . ')
    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    ret = sparql.query()
    print(ret)
    if ret.bindings:
        raise SameGroupNameException


def insertEndDeviceGroup(endDeviceGroup): #need to figure out how to put DER Functions into blazegraph too.
    '''

    :param endDeviceGroup:
    :return:
    '''
    q = (prefix + 'INSERT DATA { ')
    mRIDStr = str(endDeviceGroup.mRID)
    # Need an underscore on the ID.
    if mRIDStr[0] != '_':
        mRIDStr = '_' + mRIDStr

    checkmRIDExists(mRIDStr)
    #checkNameExists(endDeviceGroup.description)

    group = '<' + blazegraph_url + '#' + mRIDStr + '>'

    q += group + ' a c:EndDeviceGroup . ' + group + ' c:IdentifiedObject.mRID \"' + mRIDStr + '\" . ' + group + ' c:IdentifiedObject.description \"' + endDeviceGroup.description + '\" . '

    for name in endDeviceGroup.Names:
        q += group + ' c:IdentifiedObject.name \"' + name.name + '\" . '

    for device in endDeviceGroup.EndDevices:
        deviceID = str(device.mRID)
        if deviceID[0] != '_':
            deviceID = '_' + deviceID
        dv = '<' + blazegraph_url + '#' + deviceID + '>'
        q += group + ' c:EndDeviceGroup.EndDevice ' + dv + ' . '

    derFunction = '<' + blazegraph_url + '#_' + str(uuid.uuid4()) + '>'
    q += group + ' c:DERFunction ' + derFunction + ' . '
    q += derFunction + ' a c:DERFunction . '
    q += derFunction + ' c:DERFunction.connectDisconnect ' + str(endDeviceGroup.DERFunction.connectDisconnect).lower() + ' . '
    q += derFunction + ' c:DERFunction.frequencyWattCurveFunction ' + str(endDeviceGroup.DERFunction.frequencyWattCurveFunction).lower() + ' . '
    q += derFunction + ' c:DERFunction.maxRealPowerLimiting ' + str(endDeviceGroup.DERFunction.maxRealPowerLimiting).lower() + ' . '
    q += derFunction + ' c:DERFunction.rampRateControl ' + str(endDeviceGroup.DERFunction.rampRateControl).lower() + ' . '
    q += derFunction + ' c:DERFunction.reactivePowerDispatch ' + str(endDeviceGroup.DERFunction.reactivePowerDispatch).lower() + ' . '
    q += derFunction + ' c:DERFunction.realPowerDispatch ' + str(endDeviceGroup.DERFunction.realPowerDispatch).lower() + ' . '
    q += derFunction + ' c:DERFunction.voltageRegulation ' + str(endDeviceGroup.DERFunction.voltageRegulation).lower() + ' . '
    q += derFunction + ' c:DERFunction.voltVarCurveFunction ' + str(endDeviceGroup.DERFunction.voltVarCurveFunction).lower() + ' . '
    q += derFunction + ' c:DERFunction.voltWattCurveFunction ' + str(endDeviceGroup.DERFunction.voltWattCurveFunction).lower() + ' . '


    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    sparql.method = 'POST'
    ret = sparql.query()
    print(ret)


def deleteDERGroupByName(name):
    # sparql = SPARQLWrapper2(blazegraph_url)

    q = (prefix + 'DELETE Where{ ' +
         '?group c:IdentifiedObject.name \"' + name + '\" . ' +
         '?group ?property ?value . ' +
         '?group c:DERFunction ?func . ' +
         '?func ?property2 ?value2 .'
         )
    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    sparql.method = 'POST'
    ret = sparql.query()
    print(ret)


def deleteDERGroupByMrid(mrid):
    # sparql = SPARQLWrapper2(blazegraph_url)

    mrid = str(mrid)
    # Need an underscore on the ID.
    if mrid[0] != '_':
        mrid = '_' + mrid

    q = (prefix + 'DELETE Where{ ' +
         '?group c:IdentifiedObject.mRID \"' + mrid + '\" ; ' +
         '?property ?value ; ' +
         'c:DERFunction ?func . ' +
         '?func ?property2 ?value2 .'
         )

    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    sparql.method = 'POST'
    ret = sparql.query()
    print(ret)


def modifyDERGroup(endDeviceGroup):
    mRIDStr = str(endDeviceGroup.mRID)
    # Need an underscore on the ID.
    if mRIDStr[0] != '_':
        mRIDStr = '_' + mRIDStr

    i = ''
    group = '<' + blazegraph_url + '#' + mRIDStr + '>'
    for device in endDeviceGroup.EndDevices:
        deviceID = str(device.mRID)
        if deviceID[0] != '_':
            deviceID = '_' + deviceID
        dv = '<' + blazegraph_url + '#' + deviceID + '>'
        i += group + ' c:EndDeviceGroup.EndDevice ' + dv + ' . '

    derFunction = '<' + blazegraph_url + '#_' + str(uuid.uuid4()) + '>'
    i += group + ' c:DERFunction ' + derFunction + ' . '
    i += derFunction + ' a c:DERFunction . '
    i += derFunction + ' c:DERFunction.connectDisconnect ' + str(endDeviceGroup.DERFunction.connectDisconnect).lower() + ' . '
    i += derFunction + ' c:DERFunction.frequencyWattCurveFunction ' + str(endDeviceGroup.DERFunction.frequencyWattCurveFunction).lower() + ' . '
    i += derFunction + ' c:DERFunction.maxRealPowerLimiting ' + str(endDeviceGroup.DERFunction.maxRealPowerLimiting).lower() + ' . '
    i += derFunction + ' c:DERFunction.rampRateControl ' + str(endDeviceGroup.DERFunction.rampRateControl).lower() + ' . '
    i += derFunction + ' c:DERFunction.reactivePowerDispatch ' + str(endDeviceGroup.DERFunction.reactivePowerDispatch).lower() + ' . '
    i += derFunction + ' c:DERFunction.realPowerDispatch ' + str(endDeviceGroup.DERFunction.realPowerDispatch).lower() + ' . '
    i += derFunction + ' c:DERFunction.voltageRegulation ' + str(endDeviceGroup.DERFunction.voltageRegulation).lower() + ' . '
    i += derFunction + ' c:DERFunction.voltVarCurveFunction ' + str(endDeviceGroup.DERFunction.voltVarCurveFunction).lower() + ' . '
    i += derFunction + ' c:DERFunction.voltWattCurveFunction ' + str(endDeviceGroup.DERFunction.voltWattCurveFunction).lower() + ' . '

    q = (prefix + 'DELETE { ?group c:EndDeviceGroup.EndDevice ?deviceobj . ' +
                          '?group c:DERFunction ?func .' +
                          '?func ?property2 ?value2 . }' +
                  'INSERT { ' + i + ' }' +
                  'Where { ' +
         '?group c:IdentifiedObject.mRID \"' + mRIDStr + '\"; ' +
         'c:EndDeviceGroup.EndDevice ?deviceobj; ' +
         'c:DERFunction ?func . ' +
         '?func ?property2 ?value2 .'
         )

    # Update query
    q += '}'

    # Make update in triplestore.
    sparql.setQuery(q)
    sparql.method = 'POST'
    ret = sparql.query()
    print(ret)