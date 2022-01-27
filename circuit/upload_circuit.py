# Copyright (C) 2021-2022 Battelle Memorial Institute
# file: make_circuit.py

import cimhub.api as cimhub
import cimhub.CIMHubConfig as CIMHubConfig
import os
import subprocess
import stat
import shutil 

cfg_json = 'cimhubconfig.json'
CIMHubConfig.ConfigFromJsonFile (cfg_json)
ckt_mRID = '_503D6E20-F499-4CC7-8051-971E23D0BF79'
froot = 'Transactive'
cwd = os.getcwd()

cases = [
  {'root':froot, 'mRID':'503D6E20-F499-4CC7-8051-971E23D0BF79','glmvsrc': 2400.00,'bases':[4160.0],
   'export_options':' -l=1.0 -z=1.0 =h=1 -e=carson',
   'check_branches':[{'dss_link': 'LINE.LINE_L114', 'dss_bus': 'NODE_135', 'gld_link': 'LINE_LINE_L114', 'gld_bus': 'NODE_135'}]},
  ]

# upload the CIM XML file to Blazegraph
cimhub.clear_db (cfg_json)
cmd = 'curl -D- -H "Content-Type: application/xml" --upload-file {:s}.xml -X POST '.format (froot) + CIMHubConfig.blazegraph_url
os.system (cmd)
cimhub.list_feeders ()

# insert houses and DER
cimhub.insert_houses (cfg_json, ckt_mRID, 3, 0, 'Transactive_house_uuids.json', 1.0)
p1 = subprocess.Popen ('python3 allocate_der.py', shell=True)
p1.wait()
cimhub.insert_der (cfg_json, 'Transactive_der.dat')

# insert measurements
cimhub.list_measurables (cfg_json, froot, ckt_mRID)
for mtxt in ['node_v', 'lines_pq', 'switch_i', 'loads', 'machines', 'special']:
  mfile = '{:s}_{:s}.txt'.format (froot, mtxt)
  cimhub.insert_measurements (cfg_json, mfile, froot + '_msid.json')
cimhub.summarize_db (cfg_json)

