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
global deviceList

# Step 1: Establish connection to GridAPPS-D Platform:

gapps_sim = GridAPPSD("('localhost', 61613)",
                      username='system', password='manager')

# Step 2: Query

# Query for regionID and subregionID
message = {
    "requestType": "QUERY_MODEL_INFO",
    "resultFormat": "JSON",
}

response_obj = gapps_sim.get_response(t.REQUEST_POWERGRID_DATA, message)
response_obj_models = response_obj["data"]["models"] #list format

for b in response_obj_models:
    print(b['regionName'], b['regionId'])
    print(b['subRegionName'], b['subRegionId'])
    print(b['modelName'], b['modelId'])

time.sleep(2)

# Query for object (Equipment)
# Line_name
model_mrid = "_503D6E20-F499-4CC7-8051-971E23D0BF79"

# message = {
#     "modelId": model_mrid,
#     "requestType": "QUERY_OBJECT_DICT",
#     "resultFormat": "JSON",
#     "objectId": "_7357f5b6-86de-49b5-9e3c-42707475ab41"
# }

message = {
        "requestType": "QUERY_OBJECT_DICT",
        "modelId": model_mrid,
        "resultFormat": "JSON",
        "objectType": "PowerElectronicsConnection"
}
response_obj = gapps_sim.get_response(t.REQUEST_POWERGRID_DATA, message)
information = response_obj["data"]

time.sleep(2)

queryEndDevices_Model = """
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://iec.ch/TC57/CIM100#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?name ?mrid ?issmart ?upoint #?upoint
WHERE {{
  ?s a c:EndDevice .
  ?s c:IdentifiedObject.name ?name .
  ?s c:IdentifiedObject.mRID ?rawmrid .
    bind(strafter(str(?rawmrid),"_") as ?mrid)
  ?s c:EndDevice.isSmartInverter ?issmart .
  ?s c:EndDevice.UsagePoint ?upraw .
    bind(strafter(str(?upraw),"#_") as ?upoint)
  #?upraw c:IdentifiedObject.name ?upointName .
  #?upraw c:IdentifiedObject.mRID ?upointID .
  #  bind(strafter(str(?upointID),"_") as ?upoint2)
  ?equip c:Equipment.UsagePoint ?upraw .
  ?equip c:Equipment.EquipmentContainer ?container.
  ?container c:IdentifiedObject.name ?fdr .
  ?container c:IdentifiedObject.mRID ?fdrid .
  VALUES ?fdrid {{{mrid}}} .
}}
ORDER by ?name
"""

query = queryEndDevices_Model.format(mrid="\"" + model_mrid + "\"")
devices = gapps_sim.query_data(query)

time.sleep(2)
