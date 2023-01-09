# Copyright (C) 2021-2022 Battelle Memorial Institute
# file:test.py

import cimhub.api as cimhub
import cimhub.CIMHubConfig as CIMHubConfig
import os
import subprocess
import stat
import shutil 

cfg_json = 'cimhubconfig.json'
CIMHubConfig.ConfigFromJsonFile (cfg_json)
ckt_mRID = '503D6E20-F499-4CC7-8051-971E23D0BF79'
froot = 'Transactive'
cwd = os.getcwd()

cases = [
  {'root':froot, 'mRID':'503D6E20-F499-4CC7-8051-971E23D0BF79','glmvsrc': 2400.00,'bases':[4160.0],
   'export_options':' -l=1.0 -z=1.0 -h=1 -t=1 -e=carson',
   'outpath_dss': '', 'outpath_glm': './glm/', 'outpath_csv': '', 'path_xml': './',
   'check_branches':[{'dss_link': 'LINE.LINE_L114', 'dss_bus': 'NODE_135', 'gld_link': 'LINE_LINE_L114', 'gld_bus': 'NODE_135'}]},
  ]

# export and run a GridLAB-D model
shfile = './go.sh'
cimhub.make_export_script (cases, shfile)
st = os.stat (shfile)
os.chmod (shfile, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
p1 = subprocess.call (shfile, shell=True)

os.chdir(cwd)
cimhub.make_glmrun_script (cases, scriptname='./glm/checkglm.sh', bHouses=True)
shutil.copy ('../../CIMHub/support/appliance_schedules.glm', './glm/')
shfile = './glm/checkglm.sh'
st = os.stat (shfile)
os.chmod (shfile, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
os.chdir('./glm')
p1 = subprocess.call ('./checkglm.sh')

os.chdir(cwd)
cimhub.write_glm_flows (glmpath=cases[0]['outpath_glm'], 
                        rootname=cases[0]['root'], 
                        voltagebases=cases[0]['bases'], 
                        check_branches=cases[0]['check_branches'])

