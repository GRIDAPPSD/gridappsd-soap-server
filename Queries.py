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