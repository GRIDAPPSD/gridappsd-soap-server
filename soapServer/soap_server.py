"""
Example soap server using spyne.

Run with

   uwsgi --http :8000 \
         --wsgi-file soapServer.py \
         --virtualenv ~/.pyenv/versions/3.5.2/envs/zeep \
         -p 10

"""
import math

import Queries

# import time
import json
import pprint
import uuid
import DERGroupStatuses
# from lxml import etree
from statistics import mean
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
# from equipment import Equipments, SynchronousMachine, Solar, Battery
from DERGroups import DERGroups, EndDeviceGroup, EndDevice, DERFunction, Version
from exceptions import SamemRIDException, SameGroupNameException
from message import ReplyType, HeaderType, ResultType, ErrorType, LevelType, UUIDWithAttribute, VerbType, IDKindType, \
    Name
from ExecuteDERGroupsCommands import insertEndDeviceGroup, deleteDERGroupByMrid, deleteDERGroupByName, modifyDERGroup
from DERGroupsMessage import DERGroupsPayloadType, DERGroupsResponseMessageType, DERGroupsRequestMessageType
from DERGroupDispatchesMessage import DERGroupDispatchesPayloadType, DERGroupDispatchesResponseMessageType
from datetime import datetime, timedelta
from DERGroupQueries import DERGroupQueries
from DERGroupQueriesMessage import DERGroupQueriesResponseMessageType, DERGroupQueriesRequestType, \
    DERGroupQueriesPayloadType
from DERGroupStatusQueriesMessage import DERGroupStatusQueriesResponseMessageType, DERGroupStatusQueriesRequestType, DERGroupStatusQueriesPayloadType
from DERGroupForecastQueriesMessage import DERGroupForecastQueriesResponseMessageType, DERGroupForecastQueriesRequestType, DERGroupForecastQueriesPayloadType
import DifferenceMessage
from DERGroupForecastQueries import TimeIntervalKind
import DERGroupForecasts
from enums import UnitMultiplier, DERUnitSymbol, DERParameterKind
import numpy as np


conn = GridAPPSD(username="system", password="manager")
simulation_id = None
model_mrid = ''


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


def __create_difference_message(raw_message):
    '''
    create the body of the difference message
    '''

    reverse_differences = []
    forward_differences = []
    for reverse_difference in raw_message.input.message.reverse_differences:
        obj_dict = {
            "object": reverse_difference.object,
            "attribute": reverse_difference.attribute,
            "value": reverse_difference.value
        }
        reverse_differences.append(obj_dict)
    for forward_difference in raw_message.input.message.forward_differences:
        obj_dict = {
            "object": forward_difference.object,
            "attribute": forward_difference.attribute,
            "value": forward_difference.value
        }
        forward_differences.append(obj_dict)
    diff_message = {
        "timestamp": raw_message.input.message.timestamp,
        "difference_mrid": raw_message.input.message.difference_mrid,
        "reverse_differences": reverse_differences,
        "forward_differences": forward_differences
    }
    message = {
        "command": "update",
        "input": {
            "simulation_id": raw_message.input.simulation_id,
            "message": diff_message
        }
    }

    return message


def dispatchDERgroup(DERGroupDispatch, simulation_id):

    error_message = None

    # each DERGroup dispatch contains one DERGroup
    group_mrid = "_"+DERGroupDispatch.EndDeviceGroup.mRID
    group_name = DERGroupDispatch.EndDeviceGroup.Names[0].name
    DERParameter = DERGroupDispatch.EndDeviceGroup.DERMonitorableParameter.DERParameter
    flowDirection = DERGroupDispatch.EndDeviceGroup.DERMonitorableParameter.flowDirection
    if not flowDirection: flowDirection = 'forward' #by default, flow direction is "forward"
    yMultiplier = DERGroupDispatch.EndDeviceGroup.DERMonitorableParameter.yMultiplier
    yUnit = DERGroupDispatch.EndDeviceGroup.DERMonitorableParameter.yUnit
    DispatchSchedule = DERGroupDispatch.EndDeviceGroup.DERMonitorableParameter.DispatchSchedule

    ## Query equipment IDs or object IDs in each DERGroup
    query = ""
    if group_mrid:
        query = Queries.queryEquipmentBymRID.format(mRIDs="\"" + group_mrid + "\"")
    elif group_name:
        query = Queries.queryEquipmentByName.format(groupnames="\"" + group_name + "\"")
    group_exist = False
    try:
        groups = conn.query_data(query)
        group_exist = True
    except Exception as e:
        pass

    if group_exist == False:
        error_message = 'DERGroup not exist'
        return error_message

    #3 Extract query information: object id, p, q, ratedS, ratedU, type
    if 'data' in groups and 'results' in groups['data'] and 'bindings' in groups['data']['results']:

        for g in groups['data']['results']['bindings']:

            equipment_id = []

            # the following lists store the equipments to be dispatch
            equipment_id4dispatch = []
            equipment_name = []
            equipment_p = []
            equipment_q = []
            equipment_p_meas = []
            equipment_q_meas = []
            equipment_maxIFault = []
            equipment_ratedS = []
            equipment_ratedU = []
            equipment_type = []

            mRID = None
            if 'mRID' in g:
                mRID = g['mRID']['value']  # DERGroup mRID
            description = None
            if 'description' in g:
                description = g['description']['value']  # DERGroup description

            names = g['names']['value']
            model_mrid = g['modelID']['value']
            equipments = g['equipIDs']['value']

            if equipments:
                equipment_id = equipments.split('\n')

                for equip in equipment_id:

                    ## Query object dictionary
                    message = {
                        "modelId": model_mrid,
                        "requestType": "QUERY_OBJECT_DICT",
                        "resultFormat": "JSON",
                        "objectId": equip
                    }

                    # Pass query message to PowerGrid Models API
                    response_obj = conn.get_response(t.REQUEST_POWERGRID_DATA, message)
                    # response_obj_2 = conn.query_object_dictionary(model_id=model_mrid, object_id=equip)

                    if 'data' in response_obj:
                        obj_data = response_obj["data"]

                        if len(obj_data) != 1:
                            error_message = 'Return multiple objects or no object with the ID'
                            return error_message
                        else:
                            obj_data_dict = obj_data[0]

                            # if the object/equipment is PowerElectronicsConnection, query for its PowerElectronicsUnit id
                            if obj_data_dict['type'] == 'PowerElectronicsConnection' and 'PowerElectronicsConnection.PowerElectronicsUnit' in obj_data_dict:
                                # add the equipment to dispatch pipeline only if a PowerElectronicsUnit id is available
                                print('add an PowerElectronicsConnection with its PowerElectronicsUnit id ')
                                equipment_id4dispatch.append(
                                    obj_data_dict[obj_data_dict['type'] + '.PowerElectronicsUnit'])
                                equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                                equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                                equipment_maxIFault.append(float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                                equipment_ratedS.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                                equipment_ratedU.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                                equipment_type.append(obj_data_dict['type'])
                                equipment_name.append(obj_data_dict['IdentifiedObject.name'])
                            # if obj_data_dict['type'] == 'PowerElectronicsConnection':
                            #     query = Queries.queryPowerElectronicsID.format(id="\"" + equip + "\"")
                            #     pecunit = conn.query_data(query)
                            #     if 'data' in pecunit and 'results' in pecunit['data'] and 'bindings' in \
                            #             pecunit['data']['results']:
                            #         if len(pecunit['data']['results']['bindings']) == 1:
                            #             pecid = pecunit['data']['results']['bindings'][0]['pecid']['value']
                            #             equipment_id4dispatch.append(pecid)
                            #
                            #             # add the equipment to dispatch pipeline only if a PowerElectronicsUnit id is available
                            #             print('add an PowerElectronicsConnection with its PowerElectronicsUnit id ')
                            #             equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                            #             equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                            #             equipment_maxIFault.append(
                            #                 float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                            #             equipment_ratedS.append(
                            #                 float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                            #             equipment_ratedU.append(
                            #                 float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                            #             equipment_type.append(obj_data_dict['type'])
                            else:
                                # if not a PowerElectronicConnection, equipment can be a SynchronousMachine
                                print('add an SynchronousMachine with its equipment id ')
                                equipment_id4dispatch.append(
                                    equip)  # for a SynchronousMachine, equipment id can be used for dispatch
                                equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                                equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                                equipment_maxIFault.append(
                                    float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                                equipment_ratedS.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                                equipment_ratedU.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                                equipment_type.append(obj_data_dict['type'])
                                equipment_name.append(obj_data_dict['IdentifiedObject.name'])

            ## find the "current time" and "start Y values" by query measurements of equipments
            for equip in equipment_id:
                p_meas = 0
                q_meas = 0
                # Create query message to obtain measurement mRIDs for one equipment
                message = {
                    "modelId": model_mrid,
                    "requestType": "QUERY_OBJECT_MEASUREMENTS",
                    "resultFormat": "JSON",
                    "objectId": equip
                }

                # Pass query message to PowerGrid Models API
                response_obj = conn.get_response(t.REQUEST_POWERGRID_DATA, message)
                if 'data' in response_obj:
                    measurements_obj = response_obj["data"]
                    meaDict = {}
                    for k in measurements_obj:
                        if k['type'] == 'VA':
                            meaDict[k['measid']] = k

                # Query for a particular set of measurments
                message = {
                    "queryMeasurement": "simulation",
                    "queryFilter": {"simulation_id": simulation_id,
                                    "measurement_mrid": list(meaDict.keys()),
                                    "hasSimulationMessageType": "OUTPUT"},
                    "responseFormat": "JSON"
                }

                response_obj = conn.get_response(t.TIMESERIES, message)  # Pass API call
                if 'data' in response_obj:
                    time_list = [tmp['time'] for tmp in response_obj['data']]
                    simulation_current_time = max(time_list)
                    print('for equipment: ', equip)
                    print('before dispatch - at the epoch time of ', simulation_current_time)

                    for m in response_obj['data']:
                        if m['time'] == simulation_current_time:
                            print('\tmeasurement id is: ', m['measurement_mrid'])
                            print('\tangle is: ', m['angle'], ',\tmagnitude is: ', m['magnitude'])
                            ang = math.radians(float(m['angle']))
                            mag = float(m['magnitude'])
                            img = mag * math.sin(ang)
                            real = mag * math.cos(ang)
                            p_meas += real
                            q_meas += img

                # update p_meas and q_meas if exit
                equipment_p_meas.append(p_meas)
                equipment_q_meas.append(q_meas)

            # for each end device group
            print('current group status:')
            print('\tobject mRID -', equipment_id)
            print('\tobject name -', equipment_name)
            print('\tobject PEC mRID -', equipment_id4dispatch)
            print('\tp - ', equipment_p)
            print('\tq - ', equipment_q)
            print('\tp_meas - ', equipment_p_meas)
            print('\tq_meas - ', equipment_q_meas)
            print('\tratedS - ', equipment_ratedS)
            print('\tratedU - ', equipment_ratedU)
            print('\tmaxIFault - ', equipment_maxIFault)
            print('\ttype - ', equipment_type)

            ## dispatch the equipments in End Device Group
            # create difference messages
            message_list = []
            input_topic = t.simulation_input_topic(simulation_id)

            # one dispatch may contain more than one dispatchschdule, and one schdule may contain more than one curvedata
            for schedule in DispatchSchedule:
                curveStyleKind = schedule.curveStyleKind
                startTime = int(schedule.startTime.timestamp())
                print('Dispatch Schedule start time: ', startTime)
                # startTime = int(simulation_current_time) + 20  # dispatch after 20 seconds
                # print('Dispatch Schedule start time: ', startTime)
                timeIntervalDuration = int(schedule.timeIntervalDuration)
                timeIntervalUnit = schedule.timeIntervalUnit
                DERCurveData_Number = []  # each dispatch can have >= 1 CurveData
                DERCurveData_Yvalue = []
                for i_curve in range(len(schedule.DERCurveData)):
                    DERCurveData_Number.append(schedule.DERCurveData[i_curve].intervalNumber)
                    DERCurveData_Yvalue.append(schedule.DERCurveData[i_curve].nominalYValue)

                # trim solar objects from objects if DERParameter = 'activePower' and flowDirection = 'forward'
                if DERParameter == 'activePower' and flowDirection == 'forward':
                    ind_tmp = []
                    for i in range(len(equipment_name)):
                        print('check: ', equipment_name[i])
                        if 'Rooftop' not in equipment_name[i]:
                            print('keep', equipment_name[i])
                            ind_tmp.append(i)
                    if not ind_tmp:
                        error_message = 'All object/equipment are trimmed'
                        return error_message
                    equipment_id4dispatch = [equipment_id4dispatch[i] for i in ind_tmp]
                    equipment_name = [equipment_name[i] for i in ind_tmp]
                    equipment_p = [equipment_p[i] for i in ind_tmp]
                    equipment_q = [equipment_q[i] for i in ind_tmp]
                    equipment_maxIFault = [equipment_maxIFault[i] for i in ind_tmp]
                    equipment_ratedS = [equipment_ratedS[i] for i in ind_tmp]
                    equipment_ratedU = [equipment_ratedU[i] for i in ind_tmp]
                    equipment_type = [equipment_type[i] for i in ind_tmp]

                # determine which attribute to dispatch
                if DERParameter == 'activePower' and yUnit == 'W':
                    attribute2dispatch = '.p'
                elif DERParameter == 'reactivePower' and yUnit == 'VAr':
                    attribute2dispatch = '.q'
                else:
                    error_message = "Unknown DERParameter and yUnit combination"
                    return error_message
                # modify nominal Y values according to yMultiplier
                if not yMultiplier:
                    pass
                elif yMultiplier == 'k':
                    DERCurveData_Yvalue = [i * 1000 for i in DERCurveData_Yvalue]
                else:
                    error_message = "Unknown yMultiplier"
                    return error_message
                # modify nominal Y values according to flowDirection
                if flowDirection == 'forward':
                    pass
                elif flowDirection == 'reverse':
                    DERCurveData_Yvalue = [i * -1 for i in DERCurveData_Yvalue]
                else:
                    error_message = "Unknown flowDirection"
                    return error_message

                # if curveStyleKind == 'straightLineYValues', one needs the start Y values for the 1st interval
                # # option 1: use dictionaries
                # if attribute2dispatch == '.p':
                #     startYvalue = equipment_p
                # else:  # attribute2dispatch == '.q':
                #     startYvalue = equipment_q
                # option 2: use measurements
                if attribute2dispatch == '.p':
                    startYvalue = equipment_p_meas
                else:  # attribute2dispatch == '.q':
                    startYvalue = equipment_q_meas

                # determine time interval duration of each interval
                if timeIntervalUnit == 's':
                    timeIntervalDuration_num = int(timeIntervalDuration)
                elif timeIntervalUnit == 'm':
                    timeIntervalDuration_num = int(timeIntervalDuration) * 60
                elif timeIntervalUnit == 'h':
                    timeIntervalDuration_num = int(timeIntervalDuration) * 3600
                else:
                    error_message = "Unknown timeIntervalUnit"
                    return error_message
                if timeIntervalDuration_num < 3:
                    error_message = "Interval time duraction < 3 seconds"
                    return error_message
                # determine all steps for all intervals for all equipments
                if curveStyleKind == 'constantYValue':
                    list_timestamp = [i * timeIntervalDuration_num + startTime for i in
                                      range(len(DERCurveData_Yvalue))]
                    list_nominalyvalue = []
                    for i_step in range(len(DERCurveData_Yvalue)):
                        Yvalue_end_sum = DERCurveData_Yvalue[i_step]
                        list_nominalyvalue_step = [
                            Yvalue_end_sum * equipment_ratedS[i_equip] / (sum(equipment_ratedS)) \
                            for i_equip in range(len(equipment_ratedS))]
                        list_nominalyvalue.append(list_nominalyvalue_step)
                elif curveStyleKind == 'straightLineYValues':
                    list_timestamp = []
                    list_nominalyvalue = []
                    n_steps = int(
                        timeIntervalDuration_num / 3)  # determine how many steps in each time interval (every 3 seconds)
                    if n_steps > 10: n_steps = 10
                    for i in range(len(DERCurveData_Yvalue)):
                        if i == 0:
                            Yvalue_start = startYvalue  # list (length = equipment_id4dispatch)
                        else:
                            Yvalue_start = list_nominalyvalue_step  # list (length = equipment_id4dispatch)
                        Yvalue_end = [
                            DERCurveData_Yvalue[i] * equipment_ratedS[i_equip] / (sum(equipment_ratedS)) \
                            for i_equip in
                            range(len(equipment_ratedS))]  # list (length = equipment_id4dispatch)
                        for j in range(n_steps):
                            list_timestamp.append(
                                j * 3 + i * timeIntervalDuration_num + startTime)  # send difference message every 3 seconds
                            list_nominalyvalue_step = [Yvalue_start[i_equip] + (j + 1) * (
                                        Yvalue_end[i_equip] - Yvalue_start[i_equip]) / n_steps \
                                                       for i_equip in range(
                                    len(equipment_ratedS))]  # list (length = equipment_id4dispatch)
                            list_nominalyvalue.append(list_nominalyvalue_step)
                else:
                    error_message = "Unknown curveStyleKind"
                    return error_message

                for i_step in range(len(list_timestamp)):
                    timestamp = list_timestamp[i_step]  # int
                    nominalyvalues = list_nominalyvalue[i_step]  # list (length = equipment_id4dispatch)
                    if i_step == 0:
                        nominalyvalues_laststep = startYvalue
                    else:
                        nominalyvalues_laststep = list_nominalyvalue[i_step - 1]

                    difference_mrid = ''
                    reverse_differences = []
                    forward_differences = []
                    for i_equip in range(len(equipment_id4dispatch)):
                        object_id = equipment_id4dispatch[i_equip]
                        # object_id = "_EC5E71C4-3B3E-48EB-AD97-5D82B0549A49"
                        # object_id = object_id.strip('_')
                        attribute = equipment_type[i_equip] + attribute2dispatch
                        reverse_value = nominalyvalues_laststep[i_equip]
                        reverse_differences.append(
                            DifferenceMessage.OBJECT_DICT(object_id, attribute, reverse_value))
                        forward_value = nominalyvalues[i_equip]
                        forward_differences.append(
                            DifferenceMessage.OBJECT_DICT(object_id, attribute, forward_value))

                    message_message = DifferenceMessage.MESSAGE(timestamp, difference_mrid, reverse_differences,
                                                                forward_differences)
                    message_input = DifferenceMessage.INPUT(simulation_id, message_message)
                    message_list.append(DifferenceMessage.DIFFERENCEMESSAGE('update', message_input))

            for message in message_list:
                # convert class to message
                message = __create_difference_message(message)
                print(json.dumps(message, indent=4))
                # print(message)

                # send message to simulation input API channel
                response_obj = conn.send(input_topic, message)

    return error_message


# class ExecuteSimulationService(ServiceBase):
#
#     @rpc(Unicode)
#     def sendSimuID(ctx, id=None, **kwargs):
#
#         global simulation_id
#         if id is not None:
#             simulation_id = id
#
#         # print(simulation_id)


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


class ExecuteDERGroupDispatchesService(ServiceBase):

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

            # query the running simulation id
            global simulation_id
            simulation_exist = False
            message = {
                "query": "select * from log where source like \"%gov.pnnl.goss.gridappsd.simulation.SimulationProcess%\" order by timestamp desc limit 1"}
            response_obj = conn.get_response(t.LOGS, message)
            if 'data' in response_obj.keys() and len(response_obj["data"]) > 0:
                simulation = response_obj["data"][0]
                if 'process_id' and 'process_status' in simulation:
                    # simulation_id = simulation['process_id']
                    tmp = simulation['process_id']
                    simulation_id = ''.join(filter(str.isdigit, tmp))
                    simulation_status = simulation['process_status']
                    print('simulation ID: ', simulation_id, ', status: ', simulation_status)
                    if simulation_status == 'RUNNING':
                        simulation_exist = True

            # execute each dispatch
            if simulation_exist:
                try:
                    error_message = dispatchDERgroup(i, simulation_id)
                    if error_message:
                        error = True
                        eid = UUIDWithAttribute(objectType="DERGroupDispatch", value=i.mRID, kind=IDKindType.UUID)
                        reason = error_message
                except SamemRIDException:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroupDispatch", value=i.mRID, kind=IDKindType.UUID)
                    reason = 'Same mRID Exception'
                except Exception as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroupDispatch")
                    reason = str(ex)
                    print(ex)
            else:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroupDispatch")
                reason = 'No running simulation'

        re.Header = HeaderType(verb=VerbType.REPLY, noun="DERGroupDispatches", timestamp=datetime.now(), messageID=uuid.uuid4(),
                               correlationID=uuid.uuid4())
        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            # reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule',ID=eid)
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason=reason, ID=eid)

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

                            # import time

                            # start_time = str(int(time.time()) - 10)  # Start query from 10 sec ago
                            # end_time = str(int(time.time()))
                            # start_time = '1645725066'
                            # end_time = '1645725067'


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
                            tt = datetime.utcfromtimestamp(v['timestamp']).strftime('%Y-%m-%dT%H:%M:%S%z')
                            vv = round(v['value'], 2)
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


    # @staticmethod
    # def build_response_payload(groups):
    #     endgroups = []
    #     for g in groups['data']['results']['bindings']:
    #         mRID = None
    #         if 'mRID' in g:
    #             mRID = g['mRID']['value']
    #         description = None
    #         if 'description' in g:
    #             description = g['description']['value']
    #         names = g['names']['value']
    #         name = []
    #         if names:
    #             nms = names.split('\n')
    #             for nm in nms:
    #                 name.append(Name(name=nm))
    #         devices = g['devices']['value']
    #         endDevices = []
    #         if devices:
    #             dvcs = devices.split('\n')
    #             for dd in dvcs:
    #                 ids = dd.split(',')
    #                 endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
    #         funcs = g['funcs']['value']
    #         derfuncs = dict()
    #         if funcs:
    #             fs = funcs.split('\n')
    #             for ff in fs:
    #                 func = ff.split(',')
    #                 if func[1] == 'true':
    #                     derfuncs[func[0]] = True
    #                 else:
    #                     derfuncs[func[0]] = False
    #             derfunc = DERFunction(connectDisconnect=derfuncs['connectDisconnect'],
    #                                   frequencyWattCurveFunction=derfuncs['frequencyWattCurveFunction'],
    #                                   maxRealPowerLimiting=derfuncs['maxRealPowerLimiting'],
    #                                   rampRateControl=derfuncs['rampRateControl'],
    #                                   reactivePowerDispatch=derfuncs['reactivePowerDispatch'],
    #                                   realPowerDispatch=derfuncs['realPowerDispatch'],
    #                                   voltageRegulation=derfuncs['voltageRegulation'],
    #                                   voltVarCurveFunction=derfuncs['voltVarCurveFunction'],
    #                                   voltWattCurveFunction=derfuncs['voltWattCurveFunction'])
    #         else:
    #             derfunc = None
    #         newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=name,
    #                               DERFunction=derfunc)
    #         endgroups.append(newgroup)
    #     if endgroups:
    #         dergroups = DERGroups(endDeviceGroup=endgroups)
    #     else:
    #         dergroups = DERGroups(endDeviceGroup=None)
    #
    #     re = DERGroupQueriesPayloadType(dERGroups=dergroups)
    #     return re


def _get_unit_by_derParameter(param):
    if param == DERParameterKind.activePower:
        return 'W'
    # elif param == DERParameterKind.apparentPower:
    #     return 'VA'
    elif param == DERParameterKind.reactivePower:
        return 'VAr'
    # elif param == DERParameterKind.voltage:
    #     return 'V'
    elif param == DERParameterKind.stateOfCharge:
        return ''
    else:
        return ''


def _derFunction_parameter_convert(param):
    if param == 'reactivePowerDispatch':
        return DERParameterKind.reactivePower
    elif param == 'realPowerDispatch':
        return DERParameterKind.activePower
    # elif param == 'voltageRegulation':
    #     return DERParameterKind.voltage
    else:
        return param


# def adjusted_mps(mps):
#     return mps * (wtg_h2/wtg_h1) ** wtg_alpha


def _get_hub_kw(mps):
    return np.interp (mps,
    [0.0,2.9,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5,10.0,10.5,11.0,24.9,25.0,100.0],
    [ 0, 0, 25, 89,171,269,389,533,704,906,1136,1400,1674,1934,2160,2316,2416,2477,2514,2530, 0, 0], 0, 0)


# def get_wind_est (mps):
#     est = 0.0
#     if use_wtg:
#         hub_mps = adjusted_mps (mps)
#         est = get_hub_kw (hub_mps)
#     if est <= 0.0:
#         est = 1.0 # a negligible kW value; it can not be zero
#     return est


class QueryDERGroupForecastsService(ServiceBase):
    @rpc(HeaderType, DERGroupForecastQueriesRequestType, _returns=DERGroupForecastQueriesResponseMessageType)
    def QueryDERGroupForecasts(ctx, Header=None, Request=None, **kwargs):
        print(Header)
        print(Request)
        names = []
        mRIDs = []
        if Request.DERGroupForecastQueries.EndDeviceGroup:
            for group in Request.DERGroupForecastQueries.EndDeviceGroup:
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
            query = Queries.queryEquipmentWithDERfuncsByName.format(groupnames="\"" + "\" \"".join(names) + "\"")
        if mRIDs:
            query = Queries.queryEquipmentWithDERfuncsBymRID.format(mRIDs="\"" + "\" \"".join(mRIDs) + "\"")
        success = False
        try:
            groups = conn.query_data(query)
            success = True
        except Exception as e:
            pass

        re = DERGroupForecastQueriesResponseMessageType
        reheader = _build_response_header(VerbType.REPLY)
        re.Header = reheader

        derParameters = []
        if Request.DERGroupForecastQueries.DERMonitorableParameter:
            for para in Request.DERGroupForecastQueries.DERMonitorableParameter:
                derParameters.append(para.DERParameter)

        weatherDict = {}
        if Request.DERGroupForecastQueries.DispatchSchedule:
            for schdl in Request.DERGroupForecastQueries.DispatchSchedule:
                startT = schdl.startTime.replace(year=2013)
                start_time = int((startT - datetime(1970, 1, 1)).total_seconds())
                interval = schdl.numberOfIntervals
                duration = schdl.timeIntervalDuration
                unit = schdl.timeIntervalUnit
                curvetype = schdl.curveStyleKind
                multiplier = 1
                if unit == TimeIntervalKind.s:
                    end_time = start_time + interval * multiplier * duration
                elif unit == TimeIntervalKind.m:
                    multiplier = 60
                    end_time = start_time + interval * multiplier * duration
                elif unit == TimeIntervalKind.h:
                    multiplier = 3600
                    end_time = start_time + interval * multiplier * duration
                elif unit == TimeIntervalKind.D:
                    multiplier = 86400
                    end_time = start_time + interval * multiplier * duration
                # elif unit == TimeIntervalKind.M:
                #     end_time = int((schedule.startTime + timedelta(months=interval * duration) - datetime(1970,1,1)).total_seconds())
                # elif unit == TimeIntervalKind.Y:
                #     multiplier = 86400

                print(start_time)
                # if 'data' in sim_data and len(sim_data['data']) > 0:
                #     start_time = sim_data['data'][-f1]['time']
                message3 = {
                    "queryMeasurement": "weather",
                    "queryFilter": {
                        "startTime": str(start_time * 1000000),
                        "endTime": str(end_time * 1000000)},
                    "responseFormat": "JSON"
                }
                weather3 = conn.get_response(t.TIMESERIES, message3)
                weatherDict = {}
                if 'data' in weather3:
                    intvl = 1
                    for w in weather3['data']:
                        diffused = w['Diffuse']
                        direct = w['DirectCH1']
                        wind = w['AvgWindSpeed']
                        if w['time'] < start_time + intvl * multiplier * duration:
                            pass
                        else:
                            intvl += 1
                        if intvl not in weatherDict:
                            weatherDict[intvl] = {}
                        if 'solar' not in weatherDict[intvl]:
                            weatherDict[intvl]['solar'] = []
                        if 'wind' not in weatherDict[intvl]:
                            weatherDict[intvl]['wind'] = []
                        weatherDict[intvl]['wind'].append(_get_hub_kw(wind))
                        weatherDict[intvl]['solar'].append((diffused + direct) * 0.010763867)

                # message1 = {
                #     "queryMeasurement": "weather",
                #     "queryFilter": {
                #         "startTime": "1357048800000000",
                #         "endTime": "1357048860000000"},
                #     "responseFormat": "JSON"
                # }
                # weather1 = conn.get_response(t.TIMESERIES, message1)
                #
                # message2 = {
                #     "queryMeasurement": "weather",
                #     "queryFilter": {
                #         "startTime": str(start_time * 1000000),
                #         "endTime": str((start_time + 60) * 1000000)},
                #     "responseFormat": "JSON"
                # }
                # weather2 = conn.get_response(t.TIMESERIES, message2)
                print('weather queries done.')

        if success:
            payload = DERGroupForecastQueriesPayloadType()
            derforecasts = DERGroupForecasts.DERGroupForecasts()
            payload.DERGroupForecasts = derforecasts
            reply = _build_reply(ResultType.OK, '0.0')

            # message = {"query":"select process_id from log where process_type like \"%goss.gridappsd.process.request.simulation%\" order by timestamp desc limit 1"}
            # response_obj = conn.get_response(t.LOGS, message)
            # if 'data' in response_obj.keys() and len(response_obj["data"]) > 0:
            #     simulation = response_obj["data"][0]
            #     if 'process_id' in simulation:
            #         simulation_id = simulation['process_id']
            # message = {
            #     "queryMeasurement": "simulation",
            #     "queryFilter": {"simulation_id": simulation_id},
            #     "responseFormat": "JSON"
            # }
            # sim_data = conn.get_response(t.TIMESERIES, message)
            if 'data' in groups and 'results' in groups['data'] and 'bindings' in groups['data']['results']:
                forecasts = []
                for g in groups['data']['results']['bindings']:
                    eddvgrps = DERGroupForecasts.EndDeviceGroup()
                    if 'names' in g and 'value' in g['names']:
                        names = g['names']['value']
                        name = []
                        if names:
                            nms = names.split('\n')
                            for nm in nms:
                                name.append(Name(name=nm))
                            eddvgrps.Names = name
                    forecast = DERGroupForecasts.DERGroupForecastClass(mRID=uuid.uuid4(), predictionCreationDate=datetime.now(), endDeviceGroup=eddvgrps)
                    forecasts.append(forecast)
                    dmps = []
                    eddvgrps.DERMonitorableParameter = dmps
                    if 'tfuncs' in g and 'value' in g['tfuncs']:
                        funcs = g['tfuncs']['value']
                        if funcs:
                            fncs = funcs.split('\n')
                            for f in fncs:
                                fs = f.split(',')
                                parameter = _derFunction_parameter_convert(fs[0])
                                if parameter in derParameters and fs[1] == 'true':
                                    uu = _get_unit_by_derParameter(parameter)
                                    dmp = DERGroupForecasts.DERMonitorableParameter(DERParameter=parameter, yMultiplier='k', yUnit=uu)
                                    dmps.append(dmp)
                                    if Request.DERGroupForecastQueries.DispatchSchedule:
                                        schedules = []
                                        dmp.DispatchSchedule = schedules
                                        for schedule in Request.DERGroupForecastQueries.DispatchSchedule:
                                            start_time = schedule.startTime
                                            interval = schedule.numberOfIntervals
                                            duration = schedule.timeIntervalDuration
                                            unit = schedule.timeIntervalUnit
                                            nminutes = duration
                                            if unit == TimeIntervalKind.h:
                                                nminutes = 60 * duration
                                            elif unit == TimeIntervalKind.D:
                                                nminutes = 1440 * duration
                                            curvetype = schedule.curveStyleKind
                                            dispatch = DERGroupForecasts.DispatchSchedule(curveStyleKind=curvetype, startTime=start_time, timeIntervalDuration=duration, timeIntervalUnit=unit)
                                            schedules.append(dispatch)
                                            curveData = []
                                            dispatch.DERCurveData = curveData
                                            for i in range(interval):
                                                data = DERGroupForecasts.DERCurveData(intervalNumber=i+1)
                                                curveData.append(data)
                                                power = [0.0] * nminutes
                                                if parameter == DERParameterKind.activePower:
                                                    if 'equipIDs' in g and 'value' in g['equipIDs']:
                                                        equips = g['equipIDs']['value']
                                                        if equips:
                                                            eqps = equips.split('\n')
                                                            for e in eqps:
                                                                es = e.split(',')
                                                                eid = es[0]
                                                                te = es[1]
                                                                if te == 'PowerElectronicsConnection':
                                                                    query = Queries.queryPECproperties.format(equipid="\"" + eid + "\"")
                                                                elif te == 'SynchronousMachine':
                                                                    query = Queries.querySynchronousMachineProperties.format(mrid="\"" + eid + "\"")
                                                                else:
                                                                    pass
                                                                properties = conn.query_data(query)
                                                                if 'data' in properties and 'results' in properties['data'] and 'bindings' in properties['data']['results']:
                                                                    if len(properties['data']['results']['bindings']) == 1 and 'type' in properties['data']['results']['bindings'][0]:
                                                                        tp = properties['data']['results']['bindings'][0]['type']['value']
                                                                        if tp == 'SynchronousMachine':
                                                                            p = float(properties['data']['results']['bindings'][0]['p']['value'])
                                                                            power = [sum(x) for x in zip(power, weatherDict[i+1]['wind'])]
                                                                        elif tp == 'BatteryUnit':
                                                                            p = float(properties['data']['results']['bindings'][0]['p']['value'])
                                                                        elif tp == 'PhotovoltaicUnit':
                                                                            pv = float(properties['data']['results']['bindings'][0]['p']['value'])
                                                                            power = [sum(x) for x in zip(power, [x * pv for x in weatherDict[i+1]['solar']])]
                                                                            # data.maxYValue = max(power)
                                                                            # data.minYValue = min(power)
                                                                            # data.nominalYValue = mean(power)
                                                                        else:
                                                                            pass
                                                data.maxYValue = max(power)
                                                data.minYValue = min(power)
                                                data.nominalYValue = mean(power)
                derforecasts.DERGroupForecast = forecasts



        else:
            payload = None
            reply = _build_reply(ResultType.FAILED, '6.1')
        re.Payload = payload
        re.Reply = reply
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
# executeSimulation = Application(
#     services=[ExecuteSimulationService],
#     tns='der.pnnl.gov',
#     name='ExecuteSimulationService',
#     in_protocol=Soap11(validator='lxml'),
#     out_protocol=Soap11()
# )
createDERGroups = Application(
    services=[CreateDERGroupsService],
    tns='der.pnnl.gov',
    name='CreateDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
createDERGroupDispatches = Application(
    services=[ExecuteDERGroupDispatchesService],
    tns='der.pnnl.gov',
    name='ExecuteDERGroupDispatchesService',
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
queryDERGroupForecasts = Application(
    services=[QueryDERGroupForecastsService],
    tns='der.pnnl.gov',
    name='QueryDERGroupForecastsService',
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
    'getModels': getModels,
    'queryDERGroupForecasts' : queryDERGroupForecasts
})

wsgi_app = WsgiMounter({
    'get': wsgi_app_get_sub,
    'create': WsgiMounter({'executeDERGroups': createDERGroups, 'executeDERGroupDispatches': createDERGroupDispatches}),
    'change': WsgiMounter({'executeDERGroups': executeDERGroups})
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
    logging.info("QueryDERGroupForecastsService wsdl is at: http://localhost:8008/get/queryDERGroupForecasts?wsdl")

    logging.info("ExecuteDERGroupDispatchesService wsdl is at: http://localhost:8008/create/executeDERGroupDispatches?wsdl")

    server = make_server('0.0.0.0', 8008, wsgi_app)
    server.serve_forever()
