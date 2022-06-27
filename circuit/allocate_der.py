from SPARQLWrapper import SPARQLWrapper2#, JSON
import cimhub.CIMHubConfig as CIMHubConfig
import sys
import math
import numpy as np

def create_der_list (cfg_file, froot, mRID, outpath, pv_size, pv_penetration):
  if outpath is not None:
    froot = './{:s}/{:s}'.format (outpath, froot)
  CIMHubConfig.ConfigFromJsonFile (cfg_file)
  sparql = SPARQLWrapper2(CIMHubConfig.blazegraph_url)

  np.random.seed (0)
  numpv = 0
  kw = 0.001 * pv_size
  kwmax = kw
  kva = 1.01 * kwmax / math.sqrt(1-0.25*0.25)
  kv = 0.208
  kvar = 0.0
  cat = 'catA'
  mode = 'CQ'

  op = open (froot + '_der.dat', 'w')
  print ('uuid_file,{:s}_der_uuid.dat'.format (froot), file=op)
  print ('feederID,{:s}'.format (mRID), file=op)
  print ('//', file=op)
  print ('//name,bus,phases(ABCs1s2),type(Battery,Photovoltaic,SynchronousMachine),kwMax,RatedkVA,RatedkV,kW,kVAR', file=op)
  print ('//  kW is taken as maximum real power', file=op)
  print ('//  for Battery,Photovoltaic: append IEEE 1547 category [catA/catB], control mode [CQ,PF,VV,VW,WVAR,AVR,VV_VW]', file=op)
  print ('//  for Battery: append RatedkWH,StoredkWH', file=op)
  print ('// name,bus,phases(ABCs1s2),type(Battery,Photovoltaic,SynchronousMachine),RatedkVA,RatedkV,kW,kVAR,RatedkWH,StoredkWH', file=op)
  print ('//', file=op)
  print ('// commercial-scale, three-phase DER connected to the primary feeder', file=op)
  print ('PV_1,    node_60, ABC, Photovoltaic,       2000.0, 2230.0, 4.16, 2000.0, 0.0, catB, CQ', file=op)
  print ('Bat_PV,  node_60, ABC, Battery,            2000.0, 2000.0, 4.16,    0.0, 0.0, catB, CQ, 8000.0, 4000.0', file=op)
  print ('WTG_1,   node_1,  ABC, SynchronousMachine, 2000.0, 2230.0, 4.16, 2000.0, 0.0', file=op)
  print ('Bat_WTG, node_1,  ABC, Battery,            2000.0, 2000.0, 4.16,    0.0, 0.0, catB, CQ, 8000.0, 4000.0', file=op)
  print ('//', file=op)
  print ('// adding rooftop PV sized {:.2f} kW at {:.2f}% penetration'.format (kwmax, 100.0 * pv_penetration), file=op)

  fidselect = """ VALUES ?fdrid {\"""" + mRID + """\"}
   ?s c:Equipment.EquipmentContainer ?fdr.
   ?fdr c:IdentifiedObject.mRID ?fdrid. """

  ####################### - EnergyConsumer
  qstr = CIMHubConfig.prefix + """SELECT ?name ?bus ?basev ?p ?q ?conn ?cnt (group_concat(distinct ?phs;separator=":") as ?phases) WHERE {"""  + fidselect + """
 ?s r:type c:EnergyConsumer.
 ?s c:IdentifiedObject.name ?name.
 ?s c:ConductingEquipment.BaseVoltage ?bv.
 ?bv c:BaseVoltage.nominalVoltage ?basev.
 ?s c:EnergyConsumer.customerCount ?cnt.
 ?s c:EnergyConsumer.p ?p.
 ?s c:EnergyConsumer.q ?q.
 ?s c:EnergyConsumer.phaseConnection ?connraw.
   bind(strafter(str(?connraw),\"PhaseShuntConnectionKind.\") as ?conn)
 OPTIONAL {?ecp c:EnergyConsumerPhase.EnergyConsumer ?s.
 ?ecp c:EnergyConsumerPhase.phase ?phsraw.
   bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }
 ?t c:Terminal.ConductingEquipment ?s.
 ?t c:Terminal.ConnectivityNode ?cn. 
 ?cn c:IdentifiedObject.name ?bus
}
GROUP BY ?name ?bus ?basev ?p ?q ?cnt ?conn
ORDER by ?p ?name
  """
#  print (qstr)
  sparql.setQuery(qstr)
  ret = sparql.query()
#  print ('\nEnergyConsumer binding keys are:',ret.variables)
  for b in ret.bindings:
    #    print (b['bus'].value,b['basev'].value,b['phases'].value,b['p'].value)
    if np.random.uniform (0, 1) <= pv_penetration:
      numpv += 1
      print ('Rooftop_{:d},{:s},s1s2,Photovoltaic,{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:s},{:s}'.format (numpv, b['bus'].value, kwmax, kva, kv, kw, kvar, cat, mode), file=op)

  op.close()
  print ('added {:d} PV sized {:.2f} kW for {:.2f}% penetration'.format (numpv, kwmax, 100.0 * pv_penetration))

# run from command line for GridAPPS-D interop circuit
if __name__ == '__main__':
  cfg_file = 'cimhubconfig.json'
  ckt_mRID = '503D6E20-F499-4CC7-8051-971E23D0BF79'
  froot = 'Transactive'
  outpath = None
  pv_size = 3000.0
  pv_penetration = 0.9
  create_der_list (cfg_file, froot, ckt_mRID, outpath, pv_size, pv_penetration)