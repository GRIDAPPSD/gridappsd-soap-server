querySynchronousMachine = """# SynchronousMachine - DistSyncMachine
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:  <http://iec.ch/TC57/CIM100#>
SELECT ?name ?bus (group_concat(distinct ?phs;separator="\\n") as ?phases) ?ratedS ?ratedU ?p ?q ?id ?fdrid WHERE {
 ?s r:type c:SynchronousMachine.
 ?s c:IdentifiedObject.name ?name.
 ?s c:Equipment.EquipmentContainer ?fdr.
 ?fdr c:IdentifiedObject.mRID ?fdridraw.
  bind(strafter(str(?fdridraw), "_") as ?fdrid).
 ?s c:SynchronousMachine.ratedS ?ratedS.
 ?s c:SynchronousMachine.ratedU ?ratedU.
 ?s c:SynchronousMachine.p ?p.
 ?s c:SynchronousMachine.q ?q. 
 bind(strafter(str(?s),"#_") as ?id).
 OPTIONAL {?smp c:SynchronousMachinePhase.SynchronousMachine ?s.
 ?smp c:SynchronousMachinePhase.phase ?phsraw.
   bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) }
 ?t c:Terminal.ConductingEquipment ?s.
 ?t c:Terminal.ConnectivityNode ?cn. 
 ?cn c:IdentifiedObject.name ?bus
}
GROUP by ?name ?bus ?ratedS ?ratedU ?p ?q ?id ?fdrid
ORDER by ?name
"""

# # another way from dermsgui.py in gridappsd-cim-interop
# # it's slower, and the eqid and id are the same
# querySynchronousMachine="""
# PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX c: <http://iec.ch/TC57/CIM100#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
# SELECT ?name ?bus ?ratedS ?ratedU ?p ?q (group_concat(distinct ?phs;separator="\\n") as ?phases) ?eqid ?fdrid WHERE {
# 	SELECT ?name ?bus ?ratedS ?ratedU ?p ?q ?eqid ?fdrid ?phs WHERE { ?s c:Equipment.EquipmentContainer ?fdr.
#  ?fdr c:IdentifiedObject.mRID ?fdrid.
#  ?s r:type c:SynchronousMachine.
#  ?s c:IdentifiedObject.name ?name.
#  ?s c:IdentifiedObject.mRID ?eqid.
#  ?s c:SynchronousMachine.ratedS ?ratedS.
#  ?s c:SynchronousMachine.ratedU ?ratedU.
#  ?s c:SynchronousMachine.p ?p.
#  ?s c:SynchronousMachine.q ?q.
#  ?t c:Terminal.ConductingEquipment ?s.
#  ?t c:Terminal.ConnectivityNode ?cn.
#  ?cn c:IdentifiedObject.name ?bus.
#  OPTIONAL {?smp c:SynchronousMachinePhase.SynchronousMachine ?s.
#  ?smp c:SynchronousMachinePhase.phase ?phsraw.
#    bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) } } ORDER BY ?name ?phs
#  } GROUP BY ?name ?bus ?ratedS ?ratedU ?p ?q ?eqid ?fdrid
#  ORDER BY ?name
# """

querySolar = """# Solar - DistSolar
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:  <http://iec.ch/TC57/CIM100#>
SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?p ?q ?id ?fdrid (group_concat(distinct ?phs;separator="\\n") as ?phases) WHERE {
 ?s r:type c:PhotovoltaicUnit.
 ?s c:IdentifiedObject.name ?name.
 ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?s.
# feeder selection options - if all commented out, query matches all feeders
#VALUES ?fdrid {"_C1C3E687-6FFD-C753-582B-632A27E28507"}  # 123 bus
#VALUES ?fdrid {"_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"}  # 13 bus
#VALUES ?fdrid {"_5B816B93-7A5F-B64C-8460-47C17D6E4B0F"}  # 13 bus assets
#VALUES ?fdrid {"_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"}  # 8500 node
#VALUES ?fdrid {"_67AB291F-DCCD-31B7-B499-338206B9828F"}  # J1
#VALUES ?fdrid {"_9CE150A8-8CC5-A0F9-B67E-BBD8C79D3095"}  # R2 12.47 3
 ?pec c:Equipment.EquipmentContainer ?fdr.
 ?fdr c:IdentifiedObject.mRID ?fdridraw.
  bind(strafter(str(?fdridraw), "_") as ?fdrid).
 ?pec c:PowerElectronicsConnection.ratedS ?ratedS.
 ?pec c:PowerElectronicsConnection.ratedU ?ratedU.
 ?pec c:PowerElectronicsConnection.maxIFault ?ipu.
 ?pec c:PowerElectronicsConnection.p ?p.
 ?pec c:PowerElectronicsConnection.q ?q.
 OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
 ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw.
   bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) }
  bind(strafter(str(?s),"#_") as ?id).
 ?t c:Terminal.ConductingEquipment ?pec.
 ?t c:Terminal.ConnectivityNode ?cn. 
 ?cn c:IdentifiedObject.name ?bus
}
GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?p ?q ?id ?fdrid
ORDER by ?name
"""

# # Another way to query solar from dermsgui.py in gridappsd-cim-interop
# # it's slower, and the eqid and id are different
# querySolar="""
# PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX c: <http://iec.ch/TC57/CIM100#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
# SELECT ?name ?uname ?bus ?ratedS ?ratedU ?p ?q (group_concat(distinct ?phs;separator="\\n") as ?phases) ?eqid ?fdrid WHERE {
# 	SELECT ?name ?uname ?bus ?ratedS ?ratedU ?p ?q ?eqid ?fdrid ?phs WHERE { ?s c:Equipment.EquipmentContainer ?fdr.
#  ?fdr c:IdentifiedObject.mRID ?fdrid.
# ?s r:type c:PowerElectronicsConnection.
#  ?s c:IdentifiedObject.name ?name.
#  ?s c:IdentifiedObject.mRID ?eqid.
#  ?peu r:type c:PhotovoltaicUnit.
#  ?peu c:IdentifiedObject.name ?uname.
#  ?s c:PowerElectronicsConnection.PowerElectronicsUnit ?peu.
#  ?s c:PowerElectronicsConnection.ratedS ?ratedS.
#  ?s c:PowerElectronicsConnection.ratedU ?ratedU.
#  ?s c:PowerElectronicsConnection.p ?p.
#  ?s c:PowerElectronicsConnection.q ?q.
#  ?t c:Terminal.ConductingEquipment ?s.
#  ?t c:Terminal.ConnectivityNode ?cn.
#  ?cn c:IdentifiedObject.name ?bus.
#  OPTIONAL {?pep c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?s.
#  ?pep c:PowerElectronicsConnectionPhase.phase ?phsraw.
# 	bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) } } ORDER BY ?name ?phs
#  } GROUP BY ?name ?uname ?bus ?ratedS ?ratedU ?p ?q ?eqid ?fdrid
#  ORDER BY ?name
# """


queryBattery = """# Storage - DistStorage
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:  <http://iec.ch/TC57/CIM100#>
SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?p ?q ?id ?fdrid (group_concat(distinct ?phs;separator="\\n") as ?phases) WHERE {
 ?s r:type c:BatteryUnit.
 ?s c:IdentifiedObject.name ?name.
 ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?s.
# feeder selection options - if all commented out, query matches all feeders
#VALUES ?fdrid {"_C1C3E687-6FFD-C753-582B-632A27E28507"}  # 123 bus
#VALUES ?fdrid {"_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"}  # 13 bus
#VALUES ?fdrid {"_5B816B93-7A5F-B64C-8460-47C17D6E4B0F"}  # 13 bus assets
#VALUES ?fdrid {"_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"}  # 8500 node
#VALUES ?fdrid {"_67AB291F-DCCD-31B7-B499-338206B9828F"}  # J1
#VALUES ?fdrid {"_9CE150A8-8CC5-A0F9-B67E-BBD8C79D3095"}  # R2 12.47 3
 ?pec c:Equipment.EquipmentContainer ?fdr.
 ?fdr c:IdentifiedObject.mRID ?fdridraw.
  bind(strafter(str(?fdridraw), "_") as ?fdrid).
 ?pec c:PowerElectronicsConnection.ratedS ?ratedS.
 ?pec c:PowerElectronicsConnection.ratedU ?ratedU.
 ?pec c:PowerElectronicsConnection.maxIFault ?ipu.
 ?s c:BatteryUnit.ratedE ?ratedE.
 ?s c:BatteryUnit.storedE ?storedE.
 ?s c:BatteryUnit.batteryState ?stateraw.
   bind(strafter(str(?stateraw),"BatteryState.") as ?state)
 ?pec c:PowerElectronicsConnection.p ?p.
 ?pec c:PowerElectronicsConnection.q ?q. 
 OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
 ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw.
   bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) }
 bind(strafter(str(?s),"#_") as ?id).
 ?t c:Terminal.ConductingEquipment ?pec.
 ?t c:Terminal.ConnectivityNode ?cn. 
 ?cn c:IdentifiedObject.name ?bus
}
GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?p ?q ?id ?fdrid
ORDER by ?name
"""

# # Another way to query battery from dermsgui.py in gridappsd-cim-interop
# # it's slower, and the eqid and id are different
# queryBattery = """
# PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX c: <http://iec.ch/TC57/CIM100#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
# SELECT ?name ?uname ?bus ?ratedS ?ratedU ?ratedE ?storedE ?p ?q (group_concat(distinct ?phs;separator="\\n") as ?phases) ?eqid ?fdrid WHERE {
# 	SELECT ?name ?uname ?bus ?ratedS ?ratedU ?ratedE ?storedE ?p ?q ?eqid ?fdrid ?phs WHERE { ?s c:Equipment.EquipmentContainer ?fdr.
#  ?fdr c:IdentifiedObject.mRID ?fdrid.
#  ?s r:type c:PowerElectronicsConnection.
#  ?s c:IdentifiedObject.name ?name.
#  ?s c:IdentifiedObject.mRID ?eqid.
#  ?peu r:type c:BatteryUnit.
#  ?peu c:IdentifiedObject.name ?uname.
#  ?s c:PowerElectronicsConnection.PowerElectronicsUnit ?peu.
#  ?s c:PowerElectronicsConnection.ratedS ?ratedS.
#  ?s c:PowerElectronicsConnection.ratedU ?ratedU.
#  ?s c:PowerElectronicsConnection.p ?p.
#  ?s c:PowerElectronicsConnection.q ?q.
#  ?peu c:BatteryUnit.ratedE ?ratedE.
#  ?peu c:BatteryUnit.storedE ?storedE.
#  ?t c:Terminal.ConductingEquipment ?s.
#  ?t c:Terminal.ConnectivityNode ?cn.
#  ?cn c:IdentifiedObject.name ?bus.
#  OPTIONAL {?pep c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?s.
#  ?pep c:PowerElectronicsConnectionPhase.phase ?phsraw.
# 	bind(strafter(str(?phsraw),"SinglePhaseKind.") as ?phs) } } ORDER BY ?name ?phs
#  } GROUP BY ?name ?uname ?bus ?ratedS ?ratedU ?ratedE ?storedE ?p ?q ?eqid ?fdrid
#  ORDER BY ?name
# """


queryAllDERGroups = """#get all EndDeviceGroup
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description (group_concat(distinct ?name;separator="\\n") as ?names) 
 						  (group_concat(distinct ?device;separator="\\n") as ?devices)
 						  (group_concat(distinct ?func;separator="\\n") as ?funcs) 
where {
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  ?q1 c:IdentifiedObject.name ?name .
  ?q1 c:IdentifiedObject.description ?description .
  Optional{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
    ?deviceobj c:IdentifiedObject.name ?deviceName .
    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    bind(concat(strafter(str(?deviceID), "_"), ",", str(?deviceName), ",", str(?isSmart)) as ?device)
  }
  ?q1 c:DERFunction ?derFunc .
  ?derFunc ?pfunc ?vfuc .
  Filter(?pfunc !=r:type)
    bind(concat(strafter(str(?pfunc), "DERFunction."), ",", str(?vfuc)) as ?func)
}
Group by ?mRID ?description
Order by ?mRID
"""


queryDERGroupsByName = """#get all EndDeviceGroup
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description (group_concat(distinct ?name;separator="\\n") as ?names) 
 						  (group_concat(distinct ?device;separator="\\n") as ?devices)
 						  (group_concat(distinct ?func;separator="\\n") as ?funcs) 
where {{
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  ?q1 c:IdentifiedObject.name ?name .
  VALUES ?name {{{groupnames}}}
  ?q1 c:IdentifiedObject.description ?description .
  Optional{{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
    ?deviceobj c:IdentifiedObject.name ?deviceName .
    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    bind(concat(strafter(str(?deviceID), "_"), ",", str(?deviceName), ",", str(?isSmart)) as ?device)
  }}
  ?q1 c:DERFunction ?derFunc .
  ?derFunc ?pfunc ?vfuc .
  Filter(?pfunc !=r:type)
    bind(concat(strafter(str(?pfunc), "DERFunction."), ",", str(?vfuc)) as ?func)
}}
Group by ?mRID ?description
Order by ?mRID
"""


queryDERGroupsBymRID = """#get all EndDeviceGroup
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description (group_concat(distinct ?name;separator="\\n") as ?names) 
 						  (group_concat(distinct ?device;separator="\\n") as ?devices)
 						  (group_concat(distinct ?func;separator="\\n") as ?funcs) 
where {{
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  VALUES ?mRID {{{mRIDs}}}
  ?q1 c:IdentifiedObject.name ?name .
  ?q1 c:IdentifiedObject.description ?description .
  Optional{{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
    ?deviceobj c:IdentifiedObject.name ?deviceName .
    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    bind(concat(strafter(str(?deviceID), "_"), ",", str(?deviceName), ",", str(?isSmart)) as ?device)
  }}
  ?q1 c:DERFunction ?derFunc .
  ?derFunc ?pfunc ?vfuc .
  Filter(?pfunc !=r:type)
    bind(concat(strafter(str(?pfunc), "DERFunction."), ",", str(?vfuc)) as ?func)
}}
Group by ?mRID ?description
Order by ?mRID
"""


queryEndDevices = """
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://iec.ch/TC57/CIM100#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?name ?mrid ?issmart ?upoint #?upoint
WHERE {
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
}
ORDER by ?name
"""


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


queryModels = """
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://iec.ch/TC57/CIM100#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT DISTINCT ?fdr ?fdrid
WHERE {{
  ?s a c:EndDevice .
  ?s c:EndDevice.isSmartInverter ?issmart .
  ?s c:EndDevice.UsagePoint ?upraw .
    bind(strafter(str(?upraw),"#_") as ?upoint)
  ?equip c:Equipment.UsagePoint ?upraw .
  ?equip c:Equipment.EquipmentContainer ?container.
  ?container c:IdentifiedObject.name ?fdr .
  ?container c:IdentifiedObject.mRID ?fdrid .
}}
ORDER by ?fdr
"""


queryEquipmentByName = """#get all Equipment of EndDeviceGroup(s)
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description ?modelID (group_concat(distinct ?name;separator="\\n") as ?names) 
# 						  (group_concat(distinct ?device;separator="\\n") as ?devices)
# 						  (group_concat(distinct ?func;separator="\\n") as ?funcs) 
 						  (group_concat(distinct ?equipID;separator="\\n") as ?equipIDs) 
where {{
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  ?q1 c:IdentifiedObject.name ?name .
  VALUES ?name {{{groupnames}}}
  ?q1 c:IdentifiedObject.description ?description .
  Optional{{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
#    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
#    ?deviceobj c:IdentifiedObject.name ?deviceName .
#    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    ?deviceobj c:EndDevice.UsagePoint ?usg .
    ?equip c:Equipment.UsagePoint ?usg .
#    ?equip a ?tequip .
    ?equip c:Equipment.EquipmentContainer ?model .
    bind(concat(strafter(str(?equip), "#")) as ?equipID) .
#    bind(concat(strafter(str(?equip), "#"), ",", strafter(str(?tequip), "#")) as ?equipID) .
    bind(strafter(str(?model), "#") as ?modelID) .
  }}
#  ?q1 c:DERFunction ?derFunc .
#  ?derFunc ?pfunc ?vfuc .
#  Filter(?pfunc !=r:type)
#    bind(concat(strafter(str(?pfunc), "DERFunction."), ",", str(?vfuc)) as ?func)
}}
Group by ?mRID ?description ?modelID
Order by ?mRID
"""


queryEquipmentBymRID = """#get all Equipment of EndDeviceGroup(s)
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description ?modelID (group_concat(distinct ?name;separator="\\n") as ?names) 
# 						  (group_concat(distinct ?device;separator="\\n") as ?devices)
# 						  (group_concat(distinct ?func;separator="\\n") as ?funcs) 
 						  (group_concat(distinct ?equipID;separator="\\n") as ?equipIDs) 
where {{
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  VALUES ?mRID {{{mRIDs}}}
  ?q1 c:IdentifiedObject.name ?name .
  ?q1 c:IdentifiedObject.description ?description .
  Optional{{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
#    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
#    ?deviceobj c:IdentifiedObject.name ?deviceName .
#    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    ?deviceobj c:EndDevice.UsagePoint ?usg .
    ?equip c:Equipment.UsagePoint ?usg .
#    ?equip a ?tequip .
    ?equip c:Equipment.EquipmentContainer ?model .
    bind(concat(strafter(str(?equip), "#")) as ?equipID) .
#    bind(concat(strafter(str(?equip), "#"), ",", strafter(str(?tequip), "#")) as ?equipID) .
    bind(strafter(str(?model), "#") as ?modelID) .
  }}
#  ?q1 c:DERFunction ?derFunc .
#  ?derFunc ?pfunc ?vfuc .
#  Filter(?pfunc !=r:type)
#    bind(concat(strafter(str(?pfunc), "DERFunction."), ",", str(?vfuc)) as ?func)
}}
Group by ?mRID ?description ?modelID
Order by ?mRID
"""


queryPowerElectronicsID = """#get PowerElectronicsConnection ID by Equipment ID
PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://iec.ch/TC57/CIM100#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?name ?id ?pecname ?pecid
WHERE {{
  ?s c:IdentifiedObject.mRID ?id.
    VALUES ?id {{{id}}}
  ?s c:IdentifiedObject.name ?name.
  ?s c:PowerElectronicsConnection.PowerElectronicsUnit ?pec.
  ?pec c:IdentifiedObject.mRID ?pecid.
  ?pec c:IdentifiedObject.name ?pecname.
  #?pec r:type c:BatteryUnit.
  #?pec r:type c:PhotovoltaicUnit.
  #?s c:Equipment.EquipmentContainer ?fdr.
  #?fdr c:IdentifiedObject.mRID ?feeder_mrid.
  #?s c:PowerElectronicsConnection.ratedS ?ratedS.
  #?s c:PowerElectronicsConnection.ratedU ?ratedU.
  #?s c:PowerElectronicsConnection.maxIFault ?ipu.
  #?s c:PowerElectronicsConnection.p ?p.
  #?s c:PowerElectronicsConnection.q ?q.
}}
GROUP by ?name ?id ?pecname ?pecid
ORDER by ?name
"""

queryEquipmentWithDERfuncsByName = """
#get all Equipment of EndDeviceGroup(s)
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description ?modelID (group_concat(distinct ?name;separator="\\n") as ?names) 
 						  (group_concat(distinct ?equipID;separator="\\n") as ?equipIDs) 
 						  (group_concat(distinct ?tfunc2;separator="\\n") as ?tfuncs) 
where {{
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  ?q1 c:IdentifiedObject.name ?name .
  VALUES ?name {{{groupnames}}}
  ?q1 c:IdentifiedObject.description ?description .
  Optional{{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
#    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
#    ?deviceobj c:IdentifiedObject.name ?deviceName .
#    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    ?deviceobj c:EndDevice.UsagePoint ?usg .
    ?equip c:Equipment.UsagePoint ?usg .
    ?equip a ?tequip .
    ?equip c:Equipment.EquipmentContainer ?model .
#    bind(concat(strafter(str(?equip), "#")) as ?equipID) .
    bind(concat(strafter(str(?equip), "#"), ",", strafter(str(?tequip), "#")) as ?equipID) .
    bind(strafter(str(?model), "#") as ?modelID) .
  }}
  ?q1 c:DERFunction ?funcs .
  ?funcs ?tfunc ?vfuns .
  Filter(?tfunc !=r:type)
   	bind(concat(strafter(str(?tfunc), "DERFunction."), ",", str(?vfuns)) as ?tfunc2) .
}}
Group by ?mRID ?description ?modelID ?tfuncs
Order by ?mRID
"""


queryEquipmentWithDERfuncsBymRID = """
#get all Equipment of EndDeviceGroup(s)
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  r:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  c:    <http://iec.ch/TC57/CIM100#>
select ?mRID ?description ?modelID (group_concat(distinct ?name;separator="\\n") as ?names) 
 						  (group_concat(distinct ?equipID;separator="\\n") as ?equipIDs) 
 						  (group_concat(distinct ?tfunc2;separator="\\n") as ?tfuncs) 
where {
  ?q1 a c:EndDeviceGroup .
  ?q1 c:IdentifiedObject.mRID ?mRIDraw .
    bind(strafter(str(?mRIDraw), "_") as ?mRID).
  VALUES ?mRID {{{mRIDs}}}
  ?q1 c:IdentifiedObject.name ?name .
  ?q1 c:IdentifiedObject.description ?description .
  Optional{
  	?q1 c:EndDeviceGroup.EndDevice ?deviceobj .
#    ?deviceobj c:IdentifiedObject.mRID ?deviceID .
#    ?deviceobj c:IdentifiedObject.name ?deviceName .
#    ?deviceobj c:EndDevice.isSmartInverter ?isSmart .
    ?deviceobj c:EndDevice.UsagePoint ?usg .
    ?equip c:Equipment.UsagePoint ?usg .
    ?equip a ?tequip .
    ?equip c:Equipment.EquipmentContainer ?model .
#    bind(concat(strafter(str(?equip), "#")) as ?equipID) .
    bind(concat(strafter(str(?equip), "#"), ",", strafter(str(?tequip), "#")) as ?equipID) .
    bind(strafter(str(?model), "#") as ?modelID) .
  }
  ?q1 c:DERFunction ?funcs .
  ?funcs ?tfunc ?vfuns .
  Filter(?tfunc !=r:type)
   	bind(concat(strafter(str(?tfunc), "DERFunction."), ",", str(?vfuns)) as ?tfunc2) .
}
Group by ?mRID ?description ?modelID ?tfuncs
Order by ?mRID
"""


queryPECproperties = """
# query properties of a PowerElectronicsConnection, especially the type of its PowerElectronicsUnit
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:  <http://iec.ch/TC57/CIM100#>
SELECT ?name ?ratedS ?ratedU ?ipu ?p ?q ?s ?type 
WHERE {{
 ?s r:type ?t.
   bind(strafter(str(?t),"#") as ?type).
 ?s c:IdentifiedObject.name ?name.
 ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?s.
 VALUES ?equipid {{{equipid}}}.
 ?pec c:IdentifiedObject.mRID ?equipid.
 ?pec c:PowerElectronicsConnection.ratedS ?ratedS.
 ?pec c:PowerElectronicsConnection.ratedU ?ratedU.
 ?pec c:PowerElectronicsConnection.maxIFault ?ipu.
 ?pec c:PowerElectronicsConnection.p ?p.
 ?pec c:PowerElectronicsConnection.q ?q.
}}
"""


querySynchronousMachineProperties = """
# query SynchronousMachine - DistSyncMachine properties
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c:  <http://iec.ch/TC57/CIM100#>
SELECT ?name ?ratedS ?ratedU ?p ?q ?type WHERE {{
 VALUES ?equipid {{{mrid}}}.
 ?syncm c:IdentifiedObject.name ?name.
 ?syncm c:IdentifiedObject.mRID ?equipid.
 ?syncm c:SynchronousMachine.ratedS ?ratedS.
 ?syncm c:SynchronousMachine.ratedU ?ratedU.
 ?syncm c:SynchronousMachine.p ?p.
 ?syncm c:SynchronousMachine.q ?q. 
 ?syncm a ?t
   bind(strafter(str(?t),"#") as ?type).
}}
"""
