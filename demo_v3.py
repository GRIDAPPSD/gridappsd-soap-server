import argparse
import json
import logging
import sys
import time
import pytz
import stomp
import numpy as np
import math
from gridappsd import GridAPPSD, utils, DifferenceBuilder
from gridappsd import topics as t
from gridappsd.topics import simulation_input_topic, \
    simulation_output_topic, simulation_log_topic
from gridappsd.simulation import Simulation

import flask
from flask import render_template
import subprocess
import time

import Queries
import DifferenceMessage
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


# Step 0: Input information
# Dispatch information
# names = ['02072022_2'] # EndDeviceGroups
# mRIDs = ['eb72cbad-a06f-48d2-adab-1345f999db0d'] # EndDeviceGroups
names = ['03212022_1'] # EndDeviceGroups
mRIDs = ['9cad78f4-d1cd-47f0-8d03-8ff4fd4bcb17'] # EndDeviceGroups

# each DERGroup corresponds to one dispatch only
DERParameter = 'reactivePower' # 'activePower', 'reactivePower'
flowDirection = 'forward' # 'forward', 'reverse'
yMultiplier = 'k' # 'k', ''
yUnit = 'VAr' # 'W', 'VAr'
curveStyleKind = 'straightLineYValues' # "constantYValue", "straightLineYValues"
startTime = None
timeIntervalDuration = 10
timeIntervalUnit = 's'
DERCurveData_Number = [1, 2] # each dispatch can have >= 1 CurveData
DERCurveData_Yvalue = [190.0, 200.0]

# Step 1: Establish connection to GridAPPS-D Platform:
conn = GridAPPSD("('localhost', 61613)", username='system', password='manager')

# Step 2: Query RUNNING simulation and "current time"
# message = {"query": "select process_id from log where process_type like \"%goss.gridappsd.process.request.simulation%\" order by timestamp desc limit 1"}
# message = {"query": "select process_id, process_status from log where process_status = \"COMPLETE\" order by timestamp desc limit 10"}
# message = {"query": "select * from log where process_type like \"%goss.gridappsd.process.request.simulation%\" order by timestamp desc limit 10"}
message = {"query": "select * from log where source like \"%gov.pnnl.goss.gridappsd.simulation.SimulationProcess%\" order by timestamp desc limit 1"}
response_obj = conn.get_response(t.LOGS, message)
print('Query from log: ', response_obj)
simulation_exist = True # False
if 'data' in response_obj.keys() and len(response_obj["data"]) > 0:
    simulation = response_obj["data"][0]
    if 'process_id' and 'process_status' in simulation:
        # simulation_id = simulation['process_id']
        temp = simulation['process_id']
        simulation_id = ''.join(filter(str.isdigit, temp))
        simulation_status = simulation['process_status']
        print('simulation ID: ', simulation_id, ', status: ', simulation_status)
        if simulation_status == 'RUNNING':
            simulation_exist = True

# Step 3: Query equipment IDs or object IDs in each DERGroup
query = ""
if names:
    query = Queries.queryEquipmentByName.format(groupnames="\"" + "\" \"".join(names) + "\"")
elif mRIDs:
    query = Queries.queryEquipmentBymRID.format(mRIDs="\"" + "\" \"".join(mRIDs) + "\"")
group_exist = False
try:
    groups = conn.query_data(query)
    group_exist = True
except Exception as e:
    pass

if group_exist and simulation_exist:

    # Step 4: Extract query information: object id, p, q, ratedS, ratedU
    if 'data' in groups and 'results' in groups['data'] and 'bindings' in groups['data']['results']:

        for g in groups['data']['results']['bindings']:

            equipment_id = []

            # the following lists store the equipments to be dispatch
            equipment_id4dispatch = []
            equipment_name = []
            equipment_p = []
            equipment_q = []
            equipment_maxIFault = []
            equipment_ratedS = []
            equipment_ratedU = []
            equipment_type = []

            mRID = None
            if 'mRID' in g:
                mRID = g['mRID']['value'] # DERGroup mRID
            description = None
            if 'description' in g:
                description = g['description']['value'] # DERGroup description

            names = g['names']['value']
            model_mrid = g['modelID']['value']
            equipments = g['equipIDs']['value']

            if equipments:
                equipment_id = equipments.split('\n')

                for equip in equipment_id:

                    # Step 5: Query object dictionary
                    message = {
                        "modelId": model_mrid,
                        "requestType": "QUERY_OBJECT_DICT",
                        "resultFormat": "JSON",
                        "objectId": equip
                    }

                    # Pass query message to PowerGrid Models API
                    response_obj = conn.get_response(t.REQUEST_POWERGRID_DATA, message)
                    # response_obj = conn.query_object_dictionary(model_id=model_mrid, object_id=equip)

                    if 'data' in response_obj:
                        obj_data = response_obj["data"]
                        
                        if len(obj_data) != 1:
                            sys.exit('Error: return multiple objects or no object with the ID')
                        else:
                            obj_data_dict = obj_data[0]

                            # if the object/equipment is PowerElectronicsConnection, query for its PowerElectronicsUnit id
                            if obj_data_dict['type'] == 'PowerElectronicsConnection' and 'PowerElectronicsConnection.PowerElectronicsUnit' in obj_data_dict:
                                # add the equipment to dispatch pipeline only if a PowerElectronicsUnit id is available
                                print('add an PowerElectronicsConnection with its PowerElectronicsUnit id ')
                                equipment_id4dispatch.append(obj_data_dict[obj_data_dict['type']  + '.PowerElectronicsUnit'])
                                equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                                equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                                equipment_maxIFault.append(float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                                equipment_ratedS.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                                equipment_ratedU.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                                equipment_type.append(obj_data_dict['type'])
                                equipment_name.append(obj_data_dict['IdentifiedObject.name'])
                                # query = Queries.queryPowerElectronicsID.format(id="\"" + equip + "\"")
                                # pecunit = conn.query_data(query)
                                # if 'data' in pecunit and 'results' in pecunit['data'] and 'bindings' in pecunit['data']['results']:
                                #     if len(pecunit['data']['results']['bindings']) == 1:
                                #         pecid = pecunit['data']['results']['bindings'][0]['pecid']['value']
                                #         equipment_id4dispatch.append(pecid)
                                #
                                #         # add the equipment to dispatch pipeline only if a PowerElectronicsUnit id is available
                                #         print('add an PowerElectronicsConnection with its PowerElectronicsUnit id ')
                                #         equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                                #         equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                                #         equipment_maxIFault.append(
                                #             float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                                #         equipment_ratedS.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                                #         equipment_ratedU.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                                #         equipment_type.append(obj_data_dict['type'])
                            else:
                                # if not a PowerElectronicConnection, equipment can be a SynchronousMachine
                                print('add an SynchronousMachine with its equipment id ')
                                equipment_id4dispatch.append(equip) # for a SynchronousMachine, equipment id can be used for dispatch
                                equipment_p.append(float(obj_data_dict[obj_data_dict['type'] + '.p']))
                                equipment_q.append(float(obj_data_dict[obj_data_dict['type'] + '.q']))
                                equipment_maxIFault.append(float(obj_data_dict[obj_data_dict['type'] + '.maxIFault']))
                                equipment_ratedS.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedS']))
                                equipment_ratedU.append(float(obj_data_dict[obj_data_dict['type'] + '.ratedU']))
                                equipment_type.append(obj_data_dict['type'])
                                equipment_name.append(obj_data_dict['IdentifiedObject.name'])

            # for each end device group
            print('current group status:')
            print('\tobject mRID -', equipment_id)
            print('\tobject name -', equipment_name)
            print('\tobject PEC mRID -', equipment_id4dispatch)
            print('\tp - ', equipment_p)
            print('\tq - ', equipment_q)
            print('\tratedS - ', equipment_ratedS)
            print('\tratedU - ', equipment_ratedU)
            print('\tmaxIFault - ', equipment_maxIFault)
            print('\ttype - ', equipment_type)

            # Step 5: find the "current time" by query one measurement of one equipment
            equip = equipment_id[0]

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
                    if k['type'] == 'VA' or k['type'] == 'SoC':
                        meaDict[k['measid']] = k

            # Query for a particular set of measurments
            message = {
                "queryMeasurement": "simulation",
                "queryFilter": {"simulation_id": simulation_id,
                                "measurement_mrid": list(meaDict.keys()),
                                "hasSimulationMessageType": "OUTPUT"},
                "responseFormat": "JSON"
            }

            ########## option 1: from where differ from option 2 ##########
            response_obj = conn.get_response(t.TIMESERIES, message)  # Pass API call
            if 'data' in response_obj:
                time_list = [tmp['time'] for tmp in response_obj['data']]
                simulation_current_time = max(time_list)
                print('before dispatch - the epoch time is: ', simulation_current_time)

                for m in response_obj['data']:
                    if m['time'] == simulation_current_time:
                        print('\tmeasurement id is: ', m['measurement_mrid'])
                        print('\tangle is: ', m['angle'], ',\tmagnitude is: ', m['magnitude'])

            ########## option 2: complex ##########
            if False:
                groupedMea = {}

                returnTimestamp = -1
                parametersDict = {}
                for equip in equipment_id:

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
                            if k['type'] == 'VA' or k['type'] == 'SoC':
                                meaDict[k['measid']] = k

                    # Query for a particular set of measurments
                    message = {
                        "queryMeasurement": "simulation",
                        "queryFilter": {"simulation_id": simulation_id,
                                        "measurement_mrid": list(meaDict.keys()),
                                        "hasSimulationMessageType": "OUTPUT"},
                        "responseFormat": "JSON"
                    }

                    ########## option 2: from where differ from option 1 ##########
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
                                        print('if - current epoch time is: ', ts['time'])
                                        if ts['time'] > timestamp:
                                            latest = ts
                                    returnTimestamp = latest['time']
                                else:
                                    for ts in groupedMea[m]:
                                        print('else - current epoch time is: ', ts['time'])
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

            # Step 6: dispatch the equipments in End Device Group
            # trim solar objects from objects if DERParameter = 'activePower' and flowDirection = 'forward'
            if DERParameter == 'activePower' and flowDirection == 'forward':
                ind_tmp = []
                for i in range(len(equipment_name)):
                    print('check: ', equipment_name[i])
                    if 'Rooftop' not in equipment_name[i]:
                        print('keep', equipment_name[i])
                        ind_tmp.append(i)
                if not ind_tmp:
                    sys.exit('all object/equipment are trimmed')
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
                sys.exit("unknow DERParameter and yUnit combination")
            # modify nominal Y values according to yMultiplier
            if not yMultiplier:
                pass
            elif yMultiplier == 'k':
                DERCurveData_Yvalue = [i*1000 for i in DERCurveData_Yvalue]
            else:
                sys.exit("unknown yMultiplier")
            # modify nominal Y values according to flowDirection
            if flowDirection == 'forward':
                pass
            elif flowDirection == 'reverse':
                DERCurveData_Yvalue = [i * -1 for i in DERCurveData_Yvalue]
            else:
                sys.exit("unknown flowDirection")

            # several assumptions made for DERCurveData:
            startTime = int(simulation_current_time) + 20  # dispatch after 20 seconds
            if attribute2dispatch == '.p':
                startYvalue = equipment_p  # p, q values at the begining of the first curve data is 0
            else: # attribute2dispatch == '.q':
                startYvalue = equipment_q  # p, q values at the begining of the first curve data is 0

            # determine time interval duration of each interval
            if timeIntervalUnit == 's':
                timeIntervalDuration_num = int(timeIntervalDuration)
            elif timeIntervalUnit == 'm':
                timeIntervalDuration_num = int(timeIntervalDuration)*60
            elif timeIntervalUnit == 'h':
                timeIntervalDuration_num = int(timeIntervalDuration)*3600
            else:
                sys.exit("unknown timeIntervalUnit")
            if timeIntervalDuration_num < 3:
                sys.exit('interval time duration < 3 seconds')
            # determine all steps for all intervals for all equipments
            if curveStyleKind == 'constantYValue':
                list_timestamp = [i*timeIntervalDuration_num+startTime for i in range(len(DERCurveData_Yvalue))]
                list_nominalyvalue = []
                for i_step in range(len(DERCurveData_Yvalue)):
                    Yvalue_end_sum = DERCurveData_Yvalue[i_step]
                    list_nominalyvalue_step = [Yvalue_end_sum*equipment_ratedS[i_equip]/(sum(equipment_ratedS)) \
                                               for i_equip in range(len(equipment_ratedS))]
                    list_nominalyvalue.append(list_nominalyvalue_step)
            elif curveStyleKind == 'straightLineYValues':
                list_timestamp = []
                list_nominalyvalue = []
                n_steps = int(timeIntervalDuration_num/3) # determine how many steps in each time interval (every 3 seconds)
                if n_steps > 10: n_steps = 10
                for i in range(len(DERCurveData_Yvalue)):
                    if i == 0:
                        Yvalue_start = startYvalue # list (length = equipment_id4dispatch)
                    else:
                        Yvalue_start = list_nominalyvalue_step # list (length = equipment_id4dispatch)
                    Yvalue_end = [DERCurveData_Yvalue[i] * equipment_ratedS[i_equip] / (sum(equipment_ratedS)) \
                                  for i_equip in range(len(equipment_ratedS))] # list (length = equipment_id4dispatch)
                    for j in range(n_steps):
                        list_timestamp.append(j*3+i*timeIntervalDuration_num+startTime)  # send difference message every 3 seconds
                        list_nominalyvalue_step = [Yvalue_start[i_equip]+(j+1)*(Yvalue_end[i_equip]-Yvalue_start[i_equip])/n_steps \
                                                   for i_equip in range(len(equipment_ratedS))] # list (length = equipment_id4dispatch)
                        list_nominalyvalue.append(list_nominalyvalue_step)
            else:
                sys.exit("unknown curveStyleKind")

            # create difference messages
            message_list = []
            input_topic = simulation_input_topic(simulation_id)

            for i_step in range(len(list_timestamp)):
                timestamp = list_timestamp[i_step] # int
                nominalyvalues = list_nominalyvalue[i_step] # list (length = equipment_id4dispatch)
                if i_step == 0:
                    nominalyvalues_laststep = startYvalue
                else:
                    nominalyvalues_laststep = list_nominalyvalue[i_step-1]

                difference_mrid = ''
                reverse_differences = []
                forward_differences = []
                for i_equip in range(len(equipment_id4dispatch)):
                    object_id = equipment_id4dispatch[i_equip]
                    # object_id = "_EC5E71C4-3B3E-48EB-AD97-5D82B0549A49"
                    # object_id = object_id.strip('_')
                    attribute = equipment_type[i_equip] + attribute2dispatch
                    reverse_value = nominalyvalues_laststep[i_equip]
                    reverse_differences.append(DifferenceMessage.OBJECT_DICT(object_id, attribute, reverse_value))
                    forward_value = nominalyvalues[i_equip]
                    forward_differences.append(DifferenceMessage.OBJECT_DICT(object_id, attribute, forward_value))

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

            # Step 7: query for equipment measurements after dispatch
            time.sleep(20)
            for equip in equipment_id:

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
                        if k['type'] == 'VA' or k['type'] == 'SoC':
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
                    print('after dispatch - the epoch time is: ', simulation_current_time)

                    for m in response_obj['data']:
                        if m['time'] == simulation_current_time:
                            print('\tmeasurement id is: ', m['measurement_mrid'])
                            print('\tangle is: ', m['angle'], ',\tmagnitude is: ', m['magnitude'])










