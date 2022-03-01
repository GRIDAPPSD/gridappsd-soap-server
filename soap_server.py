"""
Example soap server using spyne.

Run with

   uwsgi --http :8000 \
         --wsgi-file soap_server.py \
         --virtualenv ~/.pyenv/versions/3.5.2/envs/zeep \
         -p 10

"""
import math

import Queries

import time
import json
import pprint
import uuid
import DERGroupStatuses
from lxml import etree

# from spyne import Application, ServiceBase, Unicode, rpc

from spyne import Application, Service, ComplexModel, rpc, ServiceBase, Iterable, Integer, Unicode, util, xml, AnyXml, \
    Array, AnyDict

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter
from gridappsd import GridAPPSD
from gridappsd import topics as t

from device import Device
from model import Model
from equipment import Equipments, SynchronousMachine, Solar, Battery
from DERGroups import DERGroups, EndDeviceGroup, EndDevice, DERFunction
from exceptions import SamemRIDException, SameGroupNameException
from message import ReplyType, HeaderType, ResultType, ErrorType, LevelType, UUIDWithAttribute, VerbType, IDKindType, \
    Name
from ExecuteDERGroupsCommands import insertEndDeviceGroup, deleteDERGroupByMrid, deleteDERGroupByName, modifyDERGroup
from DERGroupsMessage import DERGroupsPayloadType, DERGroupsResponseMessageType, DERGroupsRequestMessageType
from DERGroupDispatchesMessage import DERGroupDispatchesPayloadType, DERGroupDispatchesResponseMessageType
from datetime import datetime
from DERGroupQueries import DERGroupQueries
from DERGroupQueriesMessage import DERGroupQueriesResponseMessageType, DERGroupQueriesRequestType, \
    DERGroupQueriesPayloadType
from DERGroupStatusQueriesMessage import DERGroupStatusQueriesResponseMessageType, DERGroupStatusQueriesRequestType, DERGroupStatusQueriesPayloadType

conn = GridAPPSD(username="system", password="manager")
simulation_id = None
model_mrid = ''

# conn.subscribe()

# Devices = []


def get_DERM_devices():
    # payload = conn._build_query_payload('QUERY', queryString=Queries.querySynchronousMachine)
    # request_topic = '.'.join((t.REQUEST_DATA, "powergridmodel"))
    # results = conn.get_response(request_topic, json.dumps(payload), timeout=30)
    # pprint.pprint(results)
    #
    # payload = conn._build_query_payload('QUERY', queryString=Queries.querySolar )
    # request_topic = '.'.join((t.REQUEST_DATA, "powergridmodel"))
    # results = conn.get_response(request_topic, json.dumps(payload), timeout=30)
    # pprint.pprint(results)
    #
    # payload = conn._build_query_payload('QUERY', queryString=Queries.queryBattery )
    # request_topic = '.'.join((t.REQUEST_DATA, "powergridmodel"))
    # results = conn.get_response(request_topic, json.dumps(payload), timeout=30)
    # pprint.pprint(results)

    results = conn.query_data(Queries.querySynchronousMachine)
    pprint.pprint(results)
    results = conn.query_data(Queries.querySolar)
    pprint.pprint(results)
    results = conn.query_data(Queries.queryBattery)
    pprint.pprint(results)


def _build_response_header(verb):
    '''
    create message header
    :param verb: string. create, change, delete execute, get , reply, etc.
    :param message_id: string. UUID
    :param correlation_id: string. UUID
    :return: json string as the header
    '''

    return HeaderType(verb=verb, noun="DERGroups", timestamp=datetime.now(), messageID=uuid.uuid4(),
                      correlationID=uuid.uuid4())


def _build_reply(result, errorCode, errorLevel=None, reason=None):
    reply = ReplyType()
    reply.Result = result
    if errorLevel:
        reply.Error = ErrorType(code=errorCode)
    else:
        reply.Error = ErrorType(code=errorCode, level=errorLevel, reason=reason)
    return reply


class ExecuteSimulationService(ServiceBase):

    @rpc(Unicode)
    def sendSimuID(ctx, id=None, **kwargs):

        global simulation_id
        if id is not None:
            simulation_id = id

        # print(simulation_id)


class GetModelsService(ServiceBase):

    @rpc(_returns=Array(Model))
    def GetModels(ctx):
        models = conn.query_data(Queries.queryModels)
        modelList = []
        for m in models['data']['results']['bindings']:
            print(m)
            mm = Model(name=m['fdr']['value'], mRID=m['fdrid']['value'])
            modelList.append(mm)
        return modelList


class GetDevicesService(ServiceBase):

    @rpc(Unicode, _returns=Array(Device))
    def GetDevices(ctx, mrid=None, **kwargs):
        if mrid is not None:
            model_mrid = mrid
            query = Queries.queryEndDevices_Model.format(mrid="\"" + mrid + "\"")
        else:
            query = Queries.queryEndDevices
        devices = conn.query_data(query)
        deviceList = []
        for d in devices['data']['results']['bindings']:
            print(d)
            isSmartInverter = d['issmart']['value']
            if isSmartInverter == 'True':
                smart = True
            else:
                smart = False
            dd = Device(name=d['name']['value'], mRID=d['mrid']['value'], isSmartInverter=smart,
                        usagePoint=d['upoint']['value'])
            deviceList.append(dd)
        return deviceList
        # synchronousMachine = conn.query_data(Queries.queryEndDevices)
        # solar = conn.query_data(Queries.querySolar)
        # battery = conn.query_data(Queries.queryBattery)
        # syndeviceList = []
        # slrdeviceList = []
        # bttrydeviceList = []
        # for r in synchronousMachine['data']['results']['bindings']:
        #     d = SynchronousMachine(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
        #     syndeviceList.append(d)
        # for r in solar['data']['results']['bindings']:
        #     d = Solar(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
        #     slrdeviceList.append(d)
        # for r in battery['data']['results']['bindings']:
        #     d = Battery(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['ratedE']['value'], r['storedE']['value'], r['state']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
        #     bttrydeviceList.append(d)
        # return Equipments(syndeviceList, slrdeviceList, bttrydeviceList)


# class GetDERGroupsService(ServiceBase):
#
#     @rpc(_returns=DERGroups)
#     def GetDERGroups(ctx):
#         createdDERGroups = conn.query_data(Queries.queryAllDERGroups)
#         print(createdDERGroups)
#         groups = []
#         for g in createdDERGroups['data']['results']['bindings']:
#             mRID = g['mRID']['value']
#             description = None
#             if 'description' in g:
#                 description = g['description']['value']
#             name = g['names']['value']
#             d = g['devices']['value']
#             endDevices = []
#             if d:
#                 ds = d.split('\n')
#                 for dd in ds:
#                     ids = dd.split(',')
#                     # edNames=[]
#                     # edNames.append(Name(name=ids[1]))
#                     endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
#                 print(ds)
#             names = []
#             if name:
#                 nm = name.split('\n')
#                 for nn in nm:
#                     names.append(Name(name=nn))
#             f = g['funcs']['value']
#             funcs = dict()
#             if f:
#                 fs = f.split('\n')
#                 for ff in fs:
#                     func = ff.split(',')
#                     if func[1] == 'true':
#                         funcs[func[0]] = True
#                     else:
#                         funcs[func[0]] = False
#                 derfunc = DERFunction(connectDisconnect=funcs['connectDisconnect'],
#                                       frequencyWattCurveFunction=funcs['frequencyWattCurveFunction'],
#                                       maxRealPowerLimiting=funcs['maxRealPowerLimiting'],
#                                       rampRateControl=funcs['rampRateControl'],
#                                       reactivePowerDispatch=funcs['reactivePowerDispatch'],
#                                       realPowerDispatch=funcs['realPowerDispatch'],
#                                       voltageRegulation=funcs['voltageRegulation'],
#                                       voltVarCurveFunction=funcs['voltVarCurveFunction'],
#                                       voltWattCurveFunction=funcs['voltWattCurveFunction'])
#             newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=names,
#                                       DERFunction=derfunc)
#             groups.append(newgroup)
#         if groups:
#             return DERGroups(endDeviceGroup=groups)
#         else:
#             return DERGroups(endDeviceGroup=None)


class CreateDERGroupDispatchesService(ServiceBase):

    @rpc(HeaderType, DERGroupDispatchesPayloadType, _returns=DERGroupDispatchesResponseMessageType,
         _in_variable_names={"Payload": "Payload"})
    # @rpc(Iterable(Unicode), Iterable(Unicode), _returns=Unicode, _in_variable_names={"Payload": "Payload"})
    def CreateDERGroupDispatches(ctx, Header=None, Payload=None, **kwarg):
        re = DERGroupDispatchesResponseMessageType
        reply = ReplyType()
        error = False
        for i in Payload.DERGroupDispatches.DERGroupDispatch:

            # generate mRID for each dispatch
            if not i.mRID:
                if not i.mRID:
                    i.mRID = str(uuid.uuid4())
                    re.Payload = Payload

            # execute each dispatch
            try:
                # dispatchDERgroup(i)
                pass
            except SamemRIDException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroupDispatch", value=i.mRID, kind=IDKindType.UUID)
            except Exception as ex:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroupDispatch")
                print(ex)

        re.Header = HeaderType(verb=VerbType.REPLY, noun="DERGroupDispatches", timestamp=datetime.now(), messageID=uuid.uuid4(),
                               correlationID=uuid.uuid4())
        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule',ID=eid)

        re.Reply = reply
        return re


class CreateDERGroupsService(ServiceBase):
    # __in_header__ = Header
    # __port_types__ = ['ExecuteDERGroupsPort1']

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType,
         _in_variable_names={"Payload": "Payload"})
    # @rpc(Iterable(Unicode), Iterable(Unicode), _returns=Unicode, _in_variable_names={"Payload": "Payload"})
    def CreateDERGroups(ctx, Header=None, Payload=None, **kwarg):
        re = DERGroupsResponseMessageType
        reply = ReplyType()
        error = False
        for i in Payload.DERGroups.EndDeviceGroup:
            if not i.mRID:
                i.mRID = str(uuid.uuid4())
                re.Payload = Payload
            try:
                insertEndDeviceGroup(i)
            except SamemRIDException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.mRID, kind=IDKindType.UUID)
            except SameGroupNameException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.description, kind=IDKindType.NAME)
            except Exception as ex:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup")
                print(ex)

        re.Header = HeaderType(verb=VerbType.REPLY, noun="DERGroups", timestamp=datetime.now(), messageID=uuid.uuid4(),
                               correlationID=uuid.uuid4())
        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule',
                                    ID=eid)
        re.Reply = reply
        return re


class ExecuteDERGroupsService(ServiceBase):

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType)
    def DeleteDERGroups(ctx, Header=None, Payload=None, **kwargs):
        groups = Payload.DERGroups.EndDeviceGroup
        reply = ReplyType()
        error = False
        for g in groups:
            mrid = g.mRID
            names = g.Names
            assert names or mrid, "Must have either name or mrid specified"
            assert not (names and mrid), "Must have either name or mrid specified"
            if names:
                name = names[0]
                try:
                    deleteDERGroupByName(name.name)
                except Exception as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=name, kind=IDKindType.NAME)
            else:
                try:
                    deleteDERGroupByMrid(mrid)
                except SamemRIDException as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=mrid, kind=IDKindType.UUID)

        re = DERGroupsResponseMessageType
        re.Header = _build_response_header(VerbType.REPLY)
        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule',
                                    ID=eid)
        re.Reply = reply
        return re

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType)
    def ChangeDERGroups(ctx, Header=None, Payload=None, **kwargs):
        print(Header)
        print(Payload)
        error = False
        reply = ReplyType()

        if Payload.DERGroups.EndDeviceGroup:
            group = Payload.DERGroups.EndDeviceGroup[0]

        try:
            modifyDERGroup(group)
        except Exception as ex:
            error = True
            # eid = UUIDWithAttribute(objectType="DERGroup")

        re = DERGroupsResponseMessageType
        re.Header = _build_response_header(VerbType.REPLY)

        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule')
        re.Reply = reply
        return re


class QueryDERGroupsService(ServiceBase):
    @rpc(HeaderType, DERGroupQueriesRequestType, _returns=DERGroupQueriesResponseMessageType)
    def QueryDERGroups(ctx, Header=None, Request=None, **kwargs):
        print(Header)
        print(Request)
        names = []
        mRIDs = []
        if Request.DERGroupQueries.EndDeviceGroup:
            for group in Request.DERGroupQueries.EndDeviceGroup:
                if group:
                    if group.Names:
                        for name in group.Names:
                            names.append(name.name)
                            print(name.name)
                    elif group.mRID:
                        mRIDs.append(str(group.mRID))
                        print(group.mRID)
        if names:
            # b = "\"" + "\" \"".join(names) + "\""
            query = Queries.queryDERGroupsByName.format(groupnames="\"" + "\" \"".join(names) + "\"")
        if mRIDs:
            query = Queries.queryDERGroupsBymRID.format(mRIDs="\"" + "\" \"".join(mRIDs) + "\"")
        if not names and not mRIDs:
            query = Queries.queryAllDERGroups
        success = False
        try:
            groups = conn.query_data(query)
            success = True
        except Exception as e:
            pass
        re = DERGroupQueriesResponseMessageType
        reheader = _build_response_header(VerbType.REPLY)
        re.Header = reheader
        if success:
            payload = QueryDERGroupsService.build_response_payload(groups)
            reply = _build_reply(ResultType.OK, '0.0')
        else:
            payload = None
            reply = _build_reply(ResultType.FAILED, '6.1')
        re.Payload = payload
        re.Reply = reply
        return re

    @staticmethod
    def build_response_payload(groups):
        endgroups = []
        if 'data' in groups and 'results' in groups['data'] and 'bindings' in groups['data']['results']:
            for g in groups['data']['results']['bindings']:
                mRID = None
                if 'mRID' in g:
                    mRID = g['mRID']['value']
                description = None
                if 'description' in g:
                    description = g['description']['value']
                names = g['names']['value']
                name = []
                if names:
                    nms = names.split('\n')
                    for nm in nms:
                        name.append(Name(name=nm))
                devices = g['devices']['value']
                endDevices = []
                if devices:
                    dvcs = devices.split('\n')
                    for dd in dvcs:
                        ids = dd.split(',')
                        endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
                funcs = g['funcs']['value']
                derfuncs = dict()
                if funcs:
                    fs = funcs.split('\n')
                    for ff in fs:
                        func = ff.split(',')
                        if func[1] == 'true':
                            derfuncs[func[0]] = True
                        else:
                            derfuncs[func[0]] = False
                    derfunc = DERFunction(connectDisconnect=derfuncs['connectDisconnect'],
                                          frequencyWattCurveFunction=derfuncs['frequencyWattCurveFunction'],
                                          maxRealPowerLimiting=derfuncs['maxRealPowerLimiting'],
                                          rampRateControl=derfuncs['rampRateControl'],
                                          reactivePowerDispatch=derfuncs['reactivePowerDispatch'],
                                          realPowerDispatch=derfuncs['realPowerDispatch'],
                                          voltageRegulation=derfuncs['voltageRegulation'],
                                          voltVarCurveFunction=derfuncs['voltVarCurveFunction'],
                                          voltWattCurveFunction=derfuncs['voltWattCurveFunction'])
                else:
                    derfunc = None
                newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=name,
                                      DERFunction=derfunc)
                endgroups.append(newgroup)
        if endgroups:
            dergroups = DERGroups(endDeviceGroup=endgroups)
        else:
            dergroups = DERGroups(endDeviceGroup=None)

        re = DERGroupQueriesPayloadType(dERGroups=dergroups)
        return re


class QueryDERGroupStatusesService(ServiceBase):
    @rpc(HeaderType, DERGroupStatusQueriesRequestType, _returns=DERGroupStatusQueriesResponseMessageType)
    def QueryDERGroupStatuses(ctx, Header=None, Request=None, **kwargs):
        print(Header)
        print(Request)
        names = []
        mRIDs = []
        if Request.DERGroupStatusQueries.EndDeviceGroup:
            for group in Request.DERGroupStatusQueries.EndDeviceGroup:
                if group:
                    if group.Names:
                        for name in group.Names:
                            names.append(name.name)
                            print(name.name)
                    elif group.mRID:
                        mRIDs.append(str(group.mRID))
                        print(group.mRID)
        query = ""
        if names:
            # b = "\"" + "\" \"".join(names) + "\""
            query = Queries.queryEquipmentByName.format(groupnames="\"" + "\" \"".join(names) + "\"")
        if mRIDs:
            query = Queries.queryEquipmentBymRID.format(mRIDs="\"" + "\" \"".join(mRIDs) + "\"")
        success = False
        try:
            groups = conn.query_data(query)
            success = True
        except Exception as e:
            pass

        re = DERGroupStatusQueriesResponseMessageType
        reheader = _build_response_header(VerbType.REPLY)
        re.Header = reheader

        if success:
            payload = DERGroupStatusQueriesPayloadType()
            status = DERGroupStatuses.DERGroupStatuses()
            payload.DERGroupStatuses = status
            reply = _build_reply(ResultType.OK, '0.0')

            message = {"query":"select process_id from log where process_type like \"%goss.gridappsd.process.request.simulation%\" order by timestamp desc limit 1"}
            response_obj = conn.get_response(t.LOGS, message)
            if 'data' in response_obj.keys() and len(response_obj["data"]) > 0:
                simulation = response_obj["data"][0]
                if 'process_id' in simulation:
                    simulation_id = simulation['process_id']

            equipmentIDs = []
            if 'data' in groups and 'results' in groups['data'] and 'bindings' in groups['data']['results']:
                edgroups = []
                for g in groups['data']['results']['bindings']:
                    enddevicegroup = DERGroupStatuses.EndDeviceGroup()
                    mRID = None
                    if 'mRID' in g:
                        mRID = g['mRID']['value']
                        enddevicegroup.mRID = mRID

                    description = None
                    if 'description' in g:
                        description = g['description']['value']
                    names = g['names']['value']
                    name = []
                    if names:
                        nms = names.split('\n')
                        for nm in nms:
                            name.append(Name(name=nm))
                        enddevicegroup.Names = name
                    model_mrid = g['modelID']['value']
                    equipments = g['equipIDs']['value']
                    if equipments:
                        parameters = []
                        parametersDict = {}
                        enddevicegroup.DERMonitorableParameter = parameters
                        equipmentIDs = equipments.split('\n')
                        returnTimestamp = -1
                        for equip in equipmentIDs:
                            # detail = equip.split(',')
                            # equipmRID = detail[0]
                            # equipType = detail[1]

                            # Create query message to obtain measurement mRIDs for all switches
                            message = {
                                "modelId": model_mrid,
                                "requestType": "QUERY_OBJECT_MEASUREMENTS",
                                "resultFormat": "JSON",
                                "objectId": equip
                            }
    #                         message = '{"requestType": "QUERY_MODEL_NAMES", "resultFormat": "JSON"}'
                            # Pass query message to PowerGrid Models API
                            response_obj = conn.get_response(t.REQUEST_POWERGRID_DATA, message)
                            if 'data' in response_obj:
                                measurements_obj = response_obj["data"]
                                meaDict = {}
                                for k in measurements_obj:
                                    if k['type'] == 'VA' or k['type'] == 'SoC':
                                        meaDict[k['measid']] = k
                                # measids = [k['measid'] for k in measurements_obj if k['type'] == 'VA' or k['type'] == 'SoC']
                            # message = {
                            #     "processId": simulation_id,
                            #     "processStatus": "RUNNING",
                            #     "logLevel": "INFO"
                            # }
                            #
                            # tmess = conn.get_response(t.LOGS, message)
                            # message = {
                            #     "query": "select timestamp from log order by timestamp desc limit 1"}
                            # response_obj = conn.get_response(t.LOGS, message)

                            import time

                            # start_time = str(int(time.time()) - 10)  # Start query from 10 sec ago
                            # end_time = str(int(time.time()))
                            start_time = '1645725066'
                            end_time = '1645725067'


                            # Query for a particular set of measurments
                            message = {
                                "queryMeasurement": "simulation",
                                "queryFilter": {"simulation_id": simulation_id,
                                                "measurement_mrid": list(meaDict.keys()),
                                                "hasSimulationMessageType": "OUTPUT"},
                                "responseFormat": "JSON"
                            }

                            mea = conn.get_response(t.TIMESERIES, message)  # Pass API call
                            if 'data' in mea:
                                groupedMea = {}
                                for m in mea['data']:
                                    if m['measurement_mrid'] not in groupedMea:
                                        groupedMea[m['measurement_mrid']] = []
                                    groupedMea[m['measurement_mrid']].append(m)
                                for m in meaDict.keys():
                                    if m in groupedMea:
                                        timestamp = 0
                                        latest = {}
                                        if returnTimestamp == -1:
                                            for ts in groupedMea[m]:
                                                if ts['time'] > timestamp:
                                                    latest = ts
                                            returnTimestamp = latest['time']
                                        else:
                                            for ts in groupedMea[m]:
                                                if ts['time'] == returnTimestamp:
                                                    latest = ts
                                                    break

                                        if meaDict[m]['type'] == 'VA':
                                            ang = math.radians(float(latest['angle']))
                                            mag = float(latest['magnitude'])
                                            s = math.sin(ang)
                                            c = math.cos(ang)
                                            img = mag * s
                                            if 'img' not in parametersDict:
                                                parametersDict['img'] = {'timestamp': latest['time'], 'value': 0}
                                            parametersDict['img']['value'] += img / 1000
                                            real = mag * c
                                            if 'real' not in parametersDict:
                                                parametersDict['real'] = {'timestamp': latest['time'], 'value': 0}
                                            parametersDict['real']['value'] += real / 1000
                                        if meaDict[m]['type'] == 'SoC':
                                            # if 'Soc' not in parametersDict:
                                            #     parametersDict['Soc'] = 0
                                            print('SoC found.')
                            # equipmSID = [k for k in measurements_obj if k['eqid'] == equipmRID]

                            # # Switch position measurements (Pos)
                            # Pos_obj = [k for k in measurements_obj if k['type'] == 'Pos']
                            #
                            # # Switch phase-neutral-voltage measurements (PNV)
                            # PNV_obj = [k for k in measurements_obj if k['type'] == 'PNV']
                            #
                            # # Switch volt-ampere apparent power measurements (VA)
                            # VA_obj = [k for k in measurements_obj if k['type'] == 'VA']
                            #
                            # # Switch current measurements (A)
                            # A_obj = [k for k in measurements_obj if k['type'] == 'A']
                        for k, v in parametersDict.items():
                            tt = datetime.fromtimestamp(v['timestamp']).strftime('%Y-%m-%dT%H:%M:%S%z')
                            vv = v['value']
                            derParameter = DERGroupStatuses.DERMonitorableParameter()
                            curve = DERGroupStatuses.DERCurveData(nominalYValue=vv, timeStamp=tt)
                            derParameter.DERCurveData = curve
                            if k == 'real':
                                derParameter.DERParameter = DERGroupStatuses.DERParameterKind.activePower
                                derParameter.yMultiplier = DERGroupStatuses.UnitMultiplier.k
                                derParameter.yUnit = DERGroupStatuses.DERUnitSymbol.W
                            if k == 'img':
                                derParameter.DERParameter = DERGroupStatuses.DERParameterKind.reactivePower
                                derParameter.yMultiplier = DERGroupStatuses.UnitMultiplier.k
                                derParameter.yUnit = DERGroupStatuses.DERUnitSymbol.VAr
                            parameters.append(derParameter)
                    edgroups.append(enddevicegroup)
                status.EndDeviceGroup = edgroups
        else:
            payload = None
            reply = _build_reply(ResultType.FAILED, '6.1')
        re.Payload = payload
        re.Reply = reply
        return re


    @staticmethod
    def build_response_payload(groups):
        endgroups = []
        for g in groups['data']['results']['bindings']:
            mRID = None
            if 'mRID' in g:
                mRID = g['mRID']['value']
            description = None
            if 'description' in g:
                description = g['description']['value']
            names = g['names']['value']
            name = []
            if names:
                nms = names.split('\n')
                for nm in nms:
                    name.append(Name(name=nm))
            devices = g['devices']['value']
            endDevices = []
            if devices:
                dvcs = devices.split('\n')
                for dd in dvcs:
                    ids = dd.split(',')
                    endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
            funcs = g['funcs']['value']
            derfuncs = dict()
            if funcs:
                fs = funcs.split('\n')
                for ff in fs:
                    func = ff.split(',')
                    if func[1] == 'true':
                        derfuncs[func[0]] = True
                    else:
                        derfuncs[func[0]] = False
                derfunc = DERFunction(connectDisconnect=derfuncs['connectDisconnect'],
                                      frequencyWattCurveFunction=derfuncs['frequencyWattCurveFunction'],
                                      maxRealPowerLimiting=derfuncs['maxRealPowerLimiting'],
                                      rampRateControl=derfuncs['rampRateControl'],
                                      reactivePowerDispatch=derfuncs['reactivePowerDispatch'],
                                      realPowerDispatch=derfuncs['realPowerDispatch'],
                                      voltageRegulation=derfuncs['voltageRegulation'],
                                      voltVarCurveFunction=derfuncs['voltVarCurveFunction'],
                                      voltWattCurveFunction=derfuncs['voltWattCurveFunction'])
            else:
                derfunc = None
            newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=name,
                                  DERFunction=derfunc)
            endgroups.append(newgroup)
        if endgroups:
            dergroups = DERGroups(endDeviceGroup=endgroups)
        else:
            dergroups = DERGroups(endDeviceGroup=None)

        re = DERGroupQueriesPayloadType(dERGroups=dergroups)
        return re


# class HelloWorldService(ServiceBase):
#     @rpc(Unicode, Integer, _returns=Iterable(Unicode))
#     def say_hello(ctx, name, times):
#         """Docstrings for service methods appear as documentation in the wsdl.
#         <b>What fun!</b>
#
#         @param name the name to say hello to
#         @param times the number of times to say hello
#         @return the completed array
#         """
#
#         for i in range(times):
#             yield u'Hello, %s' % name

getModels = Application(
    services=[GetModelsService],
    tns='der.pnnl.gov',
    name='GetModelsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())
getDevices = Application(
    services=[GetDevicesService],
    tns='der.pnnl.gov',
    name='GetDevicesService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())
executeSimulation = Application(
    services=[ExecuteSimulationService],
    tns='der.pnnl.gov',
    name='ExecuteSimulationService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
createDERGroups = Application(
    services=[CreateDERGroupsService],
    tns='der.pnnl.gov',
    name='CreateDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
createDERGroupDispatches = Application(
    services=[CreateDERGroupDispatchesService],
    tns='der.pnnl.gov',
    name='CreateDERGroupDispatchesService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
# getDERGroups = Application(
#     services=[GetDERGroupsService],
#     tns='der.pnnl.gov',
#     name='GetDERGroupsService',
#     in_protocol=Soap11(validator='lxml'),
#     out_protocol=Soap11()
# )
executeDERGroups = Application(
    services=[ExecuteDERGroupsService],
    tns='der.pnnl.gov',
    name='ExecuteDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
queryDERGroups = Application(
    services=[QueryDERGroupsService],
    tns='der.pnnl.gov',
    name='QueryDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
queryDERGroupStatuses = Application(
    services=[QueryDERGroupStatusesService],
    tns='der.pnnl.gov',
    name='QueryDERGroupStatusesService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
# intr = getDevices.interface
# imports = intr.imports
#
# print('imports: ', imports)
# tns = getDevices.interface.get_tns()
# print('tns: ', tns)
# smm = getDevices.interface.service_method_map
# print('smm: ', smm)
# print(smm['{%s}GetDevices' % tns][0].service_class)
# print(smm['{%s}GetDevices' % tns][0].service_class == GetDevicesService)
# print(smm['{%s}GetDevices' % tns][0].function)
# print(smm['{%s}GetDevices' % tns][0].function == GetDevicesService.GetDevices)
# from spyne.interface.wsdl import Wsdl11
# wsdl = Wsdl11(intr)
# wsdl.build_interface_document('URL')
# wsdl_str = wsdl.get_interface_document()
# pprint.pprint(wsdl_str)
# wsdl_doc = etree.fromstring(wsdl_str)
# pprint.pprint('wsdl_doc')
# pprint.pprint(wsdl_doc)
#
# imports2 = createDERGroups.interface.imports
# print('imports2: ', imports2)
# tns2 = createDERGroups.interface.get_tns()
# print('tns2: ', tns2)
# smm2 = createDERGroups.interface.service_method_map
# print('smm2: ', smm2)
# print(smm2['{%s}CreateDERGroups' % tns2][0].service_class)
# print(smm2['{%s}CreateDERGroups' % tns2][0].function)
#
# RequestStatus = Unicode(values=['new', 'processed'], zonta='bonta')
#
#
# class DataRequest(ComplexModel):
#     status = Array(RequestStatus)
#
#
# class HelloWorldService(Service):
#     @rpc(DataRequest)
#     def some_call(ctx, dgrntcl):
#         pass
#
#
# hw = Application([HelloWorldService], 'spyne.examples.hello.soap',
#             in_protocol=Soap11(validator='lxml'),
#             out_protocol=Soap11())
#
# from spyne.util.xml import get_schema_documents
# docs = get_schema_documents([ResponseMessageType])
# print(docs)
# doc = docs['tns']
# print(doc)
# pprint.pprint(etree.tostring(doc, pretty_print=True))
#
# print(ResponseMessageType.resolve_namespace(ResponseMessageType, __name__))

wsgi_app_get_sub = WsgiMounter({
    'getDevices': getDevices,
    # 'getDERGroups': getDERGroups,
    'queryDERGroups': queryDERGroups,
    'queryDERGroupStatuses': queryDERGroupStatuses,
    'getModels': getModels
})

wsgi_app = WsgiMounter({
    'get': wsgi_app_get_sub,
    'create': WsgiMounter({'executeDERGroups': createDERGroups, 'executeDERGroupDispatches': createDERGroupDispatches}),
    'change': WsgiMounter({'executeDERGroups': executeDERGroups, 'executeSimulation': executeSimulation})
})

# application = Application(
#     services=[ExecuteDERGroupsService, ExecuteDERGroupsService1],
#     tns='http://127.0.0.1:8000',
#     name='ExecuteDERGroupsService',
#     in_protocol=Soap11(validator='lxml'),
#     out_protocol=Soap11())

# application = WsgiApplication(app)

if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    # get_DERM_devices()
    # synchronousMachine = conn.query_data(Queries.querySynchronousMachine)
    # print(type(synchronousMachine))
    # solar = conn.query_data(Queries.querySolar)
    # battery = conn.query_data(Queries.queryBattery)
    # deviceList = []
    # for r in synchronousMachine['data']['results']['bindings']:
    #     d = SynchronousMachine(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
    #     print(json.dumps(d.__json__()))
    #     deviceList.append(d)
    # for r in solar['data']['results']['bindings']:
    #     d = Solar(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['p']['value'], r['q']['value'], r['fdrid']['value'], r['phases']['value'])
    #     deviceList.append(d)
    # for r in battery['data']['results']['bindings']:
    #     d = Battery(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['ratedE']['value'], r['storedE']['value'], r['state']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
    #     deviceList.append(d)
    # v = json.dumps(deviceList, default=lambda o: o.__json__())
    # s = {v.__class__.__name__: v.__dict__ for v in deviceList}
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8008")
    logging.info("GetModelsService wsdl is at: http://localhost:8008/get/getModels?wsdl")
    logging.info("GetDevicesService wsdl is at: http://localhost:8008/get/getDevices?wsdl")
    logging.info("ExecuteSimulationService wsdl is at: http://localhost:8008/change/executeSimulation?wsdl")
    # logging.info("GetDERGroupsService wsdl is at: http://localhost:8008/get/getDERGroups?wsdl")
    logging.info("CreateDERGroupsService wsdl is at: http://localhost:8008/create/executeDERGroups?wsdl")
    logging.info("ExecuteDERGroupsService wsdl is at: http://localhost:8008/change/executeDERGroups?wsdl")
    logging.info("QueryDERGroupsService wsdl is at: http://localhost:8008/get/queryDERGroups?wsdl")
    logging.info("QueryDERGroupStatusesService wsdl is at: http://localhost:8008/get/queryDERGroupStatuses?wsdl")

    logging.info("CreateDERGroupDispatchesService wsdl is at: http://localhost:8008/create/executeDERGroupDispatches?wsdl")

    server = make_server('127.0.0.1', 8008, wsgi_app)
    server.serve_forever()
