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

# Step 2: Query object mRID

# Line_name
model_mrid = "_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D" #IEEE 123_PV

# Query for EndDevices
message = {
    "modelId": model_mrid,
    "requestType": "QUERY_OBJECT",
    "resultFormat": "JSON",
    "objectID": "_fc15a542-104c-41e6-9149-84ba968e3a6e"
}

response_obj = gapps_sim.get_response(t.REQUEST_POWERGRID_DATA, message)
information = response_obj["data"]

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
