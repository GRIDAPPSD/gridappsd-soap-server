import copy
import json

from SPARQLWrapper import SPARQLWrapper2
from derms_app import constants
from derms_app import derms_group as grp

sparql = SPARQLWrapper2(constants.blazegraph_url)

qstrDevice = constants.prefix +"""SELECT ?type ?name ?mrid WHERE {
 ?fid r:type c:Feeder.
 ?fid c:IdentifiedObject.name "ieee123pv".
 ?s c:ConnectivityNode.ConnectivityNodeContainer|c:Equipment.EquipmentContainer ?fid.
  #bind(strafter(str(?fidraw),"") as ?fid)
 ?s c:IdentifiedObject.name ?name.
 ?s c:IdentifiedObject.mRID ?mridraw.
  bind(strafter(str(?mridraw),"_") as ?mrid)
 ?s r:type ?typeraw.
  bind(strafter(str(?typeraw),"#") as ?type)
}
ORDER by ?type ?name
"""


def getDevices():
    deviceDict = {}
    sparql.setQuery(qstrDevice)
    ret = sparql.query()
    for b in ret.bindings:
        name = b['name'].value
        type = b['type'].value
        mrid = b['mrid'].value
        deviceDict[mrid] = {'name': name, 'mrid': mrid, 'type': type}
    return deviceDict


# def getDeviceSubset():
#     '''
#     read device from json file
#     :return: List of Devices
#     '''
#     with open("devices_list.json") as fp:
#         loaded_json = json.loads(fp.read())
#
#     devices_list = []
#
#     for x in loaded_json['devices']:
#         devices_list.append(Device(x['mrid'], x['name'], "ADevice"))
#
#     return devices_list
    # deviceList = []
    # deviceTypeList = []
    # sparql.setQuery(qstrDevice)
    # ret = sparql.query()
    # for b in ret.bindings:
    #     type = b['type'].value
    #     if type == 'PowerElectronicsConnection':
    #         mrid = b['mrid'].value
    #         name = b['name'].value
    #         #deviceList.append({'name': name, 'mrid': mrid, 'type': type})
    #         deviceList.append(Device(mrid, name, type))
    #     # else:
    #     #     if type not in deviceTypeList:
    #     #         deviceTypeList.append(type)
    #     #         mrid = b['mrid'].value
    #     #         name = b['name'].value
    #     #         deviceList.append({'name': name, 'mrid': mrid, 'type': type})
    # return deviceList


def writeJsonConf(configFile):
    #with open('/home/xcosmos/src/gridAppsD/6DNP3devicesconfig.json') as config:
    #    configDict = json.load(config)
    config = open('/home/xcosmos/src/gridAppsD/6DNP3devicesconfig.json').read()
    configDict = json.loads(config)
    currentDevices = configDict['dnp3']['devices']
    print(len(currentDevices))
    aDevice = copy.deepcopy(currentDevices[0])
    lastPortNumber = aDevice['communication']['port']
    availableDevices = getDevices()
    if availableDevices:
        pickedDeviceList = selectDevices(aDevice, availableDevices, lastPortNumber)
        configDict['dnp3']['devices'] = pickedDeviceList
        myDeviceConfig = open(configFile, 'w')
        print(json.dumps(configDict), file=myDeviceConfig)
        myDeviceConfig.close()

def selectDevices(aDevice, availableDevices, lastPortNumber):
    pickedDeviceList = []
    deviceTypeList = []
    for mrid, device in availableDevices.items():
        if device['type'] == 'PowerElectronicsConnection':
            thisDevice = copy.deepcopy(aDevice)
            thisDevice['mrid'] = mrid
            thisDevice['name'] = device['name']
            lastPortNumber += 1
            thisDevice['communication']['port'] = lastPortNumber
            pickedDeviceList.append((thisDevice))
        # else:
        #     if device['type'] not in deviceTypeList:
        #         deviceTypeList.append(device['type'])
        #         thisDevice = copy.deepcopy(aDevice)
        #         thisDevice['mrid'] = mrid
        #         thisDevice['name'] = device['name']
        #         lastPortNumber += 1
        #         thisDevice['communication']['port'] = lastPortNumber
        #         pickedDeviceList.append((thisDevice))
    return pickedDeviceList


if  __name__ == '__main__':
    writeJsonConf('/home/xcosmos/src/gridAppsD/myDeviceConfig.json')
    #pass