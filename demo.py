import argparse
import json
import logging
import sys
import time
import pytz
import stomp
import numpy as np
from gridappsd import GridAPPSD, utils, DifferenceBuilder
from gridappsd import topics as t
from gridappsd.topics import simulation_input_topic, \
    simulation_output_topic, simulation_log_topic
from gridappsd.simulation import Simulation

import flask
from flask import render_template
import subprocess
import time

# step 0: global parameters
global loop_break
global Pos_obj

# Step 1: Establish connection to GridAPPS-D Platform:

gapps_sim = GridAPPSD("('localhost', 61613)",
                      username='system', password='manager')

# Step 2: Query object mRID

# Line_name
model_mrid = "_C1C3E687-6FFD-C753-582B-632A27E28507"

# Query for mRID of switches:
message = {
    "modelId": model_mrid,
    "requestType": "QUERY_OBJECT_DICT",
    "resultFormat": "JSON",
    "objectType": "LoadBreakSwitch"
}
response_obj = gapps_sim.get_response(t.REQUEST_POWERGRID_DATA, message)
switch_dict = response_obj["data"]

# Filter to get mRID for switch SW2:
for index in switch_dict:
    if index["IdentifiedObject.name"] == 'sw2':
        sw_mrid = index["IdentifiedObject.mRID"]
        print('switch mRID is: ', sw_mrid)

# Step 3: submit simulation and subscribe to simulation

# Specify the GridAPPS-D Topic
# topic = t.REQUEST_SIMULATION
# topic = "goss.gridappsd.process.request.simulation"

print('current epoch time is: ', str(int(time.time())))
start_time = int(time.time())
test_start = start_time+30
test_end = start_time+60
run_config_123 = {
    "power_system_config": {
        "GeographicalRegion_name": "_73C512BD-7249-4F50-50DA-D93849B89C43",
        "SubGeographicalRegion_name": "_1CD7D2EE-3C91-3248-5662-A43EFEFAC224",
        "Line_name": "_C1C3E687-6FFD-C753-582B-632A27E28507"
    },
    "application_config": {
        "applications": []
    },
    "simulation_config": {
        "start_time": 1570041113,
        "duration": "120",
        "simulator": "GridLAB-D",
        "timestep_frequency": "1000",
        "timestep_increment": "1000",
        "run_realtime": True,
        "simulation_name": "ieee123",
        "power_flow_solver_method": "NR",
        "model_creation_config": {
            "load_scaling_factor": "1",
            "schedule_name": "ieeezipload",
            "z_fraction": "0",
            "i_fraction": "1",
            "p_fraction": "0",
            "randomize_zipload_fractions": False,
            "use_houses": False
        }
    },
    "test_config": {
        "events": [{
            "message": {
                "forward_differences": [
                    {
                        "object": "_6C1FDA90-1F4E-4716-BC90-1CCB59A6D5A9",
                        "attribute": "Switch.open",
                        "value": 1
                    }
                ],
                "reverse_differences": [
                    {
                        "object": "_6C1FDA90-1F4E-4716-BC90-1CCB59A6D5A9",
                        "attribute": "Switch.open",
                        "value": 0
                    }
                ]
            },
            "event_type": "ScheduledCommandEvent",
            "occuredDateTime": 1570041140,
            "stopDateTime": 1570041200
        }]
    },
     "service_configs": [{
        "id": "gridappsd-sensor-simulator",
        "user_options": {
            "sensors-config": {
                "_99db0dc7-ccda-4ed5-a772-a7db362e9818": {
                    "nominal-value": 100,
                    "perunit-confidence-band": 0.02,
                    "aggregation-interval": 5,
                    "perunit-drop-rate": 0.01
                },
                "_ee65ee31-a900-4f98-bf57-e752be924c4d": {},
                "_f2673c22-654b-452a-8297-45dae11b1e14": {}
            },
            "random-seed": 0,
            "default-aggregation-interval": 30,
            "passthrough-if-not-specified": False,
            "default-perunit-confidence-band": 0.01,
            "default-perunit-drop-rate": 0.05
        }
    }]
}

# 1. start the simulation by message
# simulation_obj = Simulation(gapps_sim, run_config_123)
# simulation_obj.start_simulation()
# simulation_id = simulation_obj.simulation_id
# print('simulation ID is: ', simulation_id)

# 2. start the simulation by load json file
run123_config = json.load(open("./configurations/Run123NodeFileSimAPI.json"))
simulation_obj = Simulation(gapps_sim, run123_config)
simulation_obj.start_simulation()
simulation_id = simulation_obj.simulation_id
print('simulation ID is: ', simulation_id)

# Step 4: publish to simulation input

input_topic = simulation_input_topic(simulation_id)
print('simulation input topic is: ', input_topic)

message = {"command": "pause"}
gapps_sim.send(input_topic, message)
time.sleep(2)
message = {"command": "resume"}
gapps_sim.send(input_topic, message)

# Step 5: subscribe to simulation output

output_topic = simulation_output_topic(simulation_id)
print('simulation output topic is: ', output_topic)

# Create query message to obtain measurement mRIDs for all switches
message = {
    "modelId": model_mrid,
    "requestType": "QUERY_OBJECT_MEASUREMENTS",
    "resultFormat": "JSON",
    "objectType": "LoadBreakSwitch"
}

# Query measurement mRID
response_obj = gapps_sim.get_response(t.REQUEST_POWERGRID_DATA, message)
measurements_obj = response_obj["data"]
Pos_obj = [k for k in measurements_obj if k['type'] == 'Pos']  # Switch position measurements
PNV_obj = [k for k in measurements_obj if k['type'] == 'PNV']  # Switch terminal phase-neutral-voltage measurements
VA_obj = [k for k in measurements_obj if k['type'] == 'VA']  # Switch volt-ampere apparent power measurements
A_obj = [k for k in measurements_obj if k['type'] == 'Pos']  # Switch current measurements

# subscribe to simulation output by function
def demoSubscription1(header, message):
    # Extract time and measurement values from message
    # print(message)
    timestamp = message["message"]["timestamp"]
    meas_value = message["message"]["measurements"]

    meas_mrid = list(meas_value.keys())
    # obtain list of all mrid from message

    # Filter to measurements with value of zero
    open_switches = []
    for index in Pos_obj:
        if index["measid"] in meas_value:
            mrid = index["measid"]
            power = meas_value[mrid]
            if power["value"] == 0:
                open_switches.append(index["eqname"])

    # Print message to command line
    print(".......... simulation - function ..........")
    print("Number of open switches at time", timestamp,
          ' is ', len(set(open_switches)))
gapps_sim.subscribe(output_topic, demoSubscription1)

# subscribe to simulation output by library shortcut
def demo_onmeas_func(sim, timestamp, measurements):
        open_switches = []
        for index in Pos_obj:
            if index["measid"] in measurements:
                mrid = index["measid"]
                power = measurements[mrid]
                if power["value"] == 0:
                    open_switches.append(index["eqname"])

        print("......library......")
        print("Number of open switches at time", timestamp, ' is ', len(set(open_switches)))
# simulation_obj.add_onmeasurement_callback(demo_onmeas_func)

# Step 6: subscribe to logging API
log_topic = simulation_log_topic(simulation_id)
def demoLogFunction(header, message):

    # print(message)
    processStatus = message["processStatus"]
    log_message = message["logMessage"]
    if processStatus == 'COMPLETE':
        global loop_break
        loop_break = True

    print(".......... Log message ..........")
    print(processStatus)
    print(log_message)
gapps_sim.subscribe(log_topic, demoLogFunction)

# query for process event
message = {
    "source": "ProcessEvent",
    "processId": simulation_id,
    "processStatus": "INFO",
    "logLevel": "INFO"
}
response_obj = gapps_sim.get_response(t.LOGS, message)
print(response_obj)

# Step 7: test case
# switch on and off every 5 seconds
my_open_diff = DifferenceBuilder(simulation_id)
my_open_diff.add_difference(sw_mrid, "Switch.open", 1, 0)  # Open switch given by sw_mrid
open_message = my_open_diff.get_message()

my_close_diff = DifferenceBuilder(simulation_id)
my_close_diff.add_difference(sw_mrid, "Switch.open", 0, 1)  # Close switch given by sw_mrid
close_message = my_close_diff.get_message()

loop_break = False
while True:
    time.sleep(2)
    gapps_sim.send(input_topic, open_message)
    time.sleep(2)
    gapps_sim.send(input_topic, close_message)

    # break the loop as the simulation complete
    # response_obj = gapps_sim.get_response(t.LOGS, message)
    # print(response_obj)

    if loop_break == True:
        break

print('Job Done')

# Appendix:

# # Query for Simulation Output Data with Timeseries API
# # Query for all measurements between a "startTime" and "endTime"
# topic = "goss.gridappsd.process.request.data.timeseries"  # Specify Timeseries API GridAPPS-D topic
# # Use queryFilter of "startTime" and "endTime"
# message = {
#     "queryMeasurement": "simulation",
#     "queryFilter": {
#         "simulation_id": simulation_id,
#         "startTime": "1570041110",
#         "endTime": "1570041170"},
#     "responseFormat": "JSON"
# }
# response_obj_TS = gapps_sim.get_response(topic, message)  # Pass API call



