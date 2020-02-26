"""
Example soap server using spyne.

Run with

   uwsgi --http :8000 \
         --wsgi-file soap_server.py \
         --virtualenv ~/.pyenv/versions/3.5.2/envs/zeep \
         -p 10

"""

import Queries

import time
import json
import pprint
import uuid
from lxml import etree

# from spyne import Application, ServiceBase, Unicode, rpc

from spyne import Application, Service, ComplexModel, rpc, ServiceBase, Iterable, Integer, Unicode, util, xml, AnyXml, Array, AnyDict

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter
from gridappsd import GridAPPSD
from gridappsd import topics as t

from device import Device
from equipment import Equipments, SynchronousMachine, Solar, Battery
from DERGroups import DERGroups, EndDeviceGroup, EndDevice
from exceptions import SamemRIDException, SameGroupNameException
from message import ReplyType, HeaderType, ResultType, ErrorType, LevelType, UUIDWithAttribute, VerbType, IDKindType, Name
from ExecuteDERGroupsCommands import insertEndDeviceGroup, deleteDERGroupByMrid, deleteDERGroupByName
from DERGroupsMessage import DERGroupsPayloadType, DERGroupsResponseMessageType, DERGroupsRequestMessageType
from datetime import datetime


conn = GridAPPSD()
# Devices = []


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


class GetDevicesService(ServiceBase):
    # __port_types__ = ['ExecuteDERGroupsPort']

    @rpc(_returns=Array(Device))
    def GetDevices(ctx):
        devices = conn.query_data(Queries.queryEndDevices)
        deviceList = []
        for d in devices['data']['results']['bindings']:
            print(d)
            isSmartInverter = d['issmart']['value']
            if isSmartInverter == 'True':
                smart = True
            else:
                smart = False
            dd = Device(name=d['name']['value'], mRID=d['mrid']['value'], isSmartInverter=smart, usagePoint=d['upoint']['value'])
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


class GetDERGroupsService(ServiceBase):

    @rpc(_returns=DERGroups)
    def GetDERGroups(ctx):
        createdDERGroups = conn.query_data(Queries.queryDERGroups)
        print(createdDERGroups)
        groups=[]
        for g in createdDERGroups['data']['results']['bindings']:
            mRID = g['mRID']['value']
            description = None
            if 'description' in g:
                description = g['description']['value']
            name = g['names']['value']
            d = g['devices']['value']
            endDevices = []
            if d:
                ds = d.split('\n')
                for dd in ds:
                    ids = dd.split(',')
                    # edNames=[]
                    # edNames.append(Name(name=ids[1]))
                    endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
                print(ds)
            names = []
            if name:
                nm = name.split('\n')
                for nn in nm:
                    names.append(Name(name=nn))
            newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=names)
            groups.append(newgroup)
        if groups:
            return DERGroups(endDeviceGroup=groups)
        else:
            return DERGroups(endDeviceGroup=None)



class CreateDERGroupsService(ServiceBase):
    # __in_header__ = Header
    # __port_types__ = ['ExecuteDERGroupsPort1']

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType, _in_variable_names={"Payload": "Payload"})
    # @rpc(Iterable(Unicode), Iterable(Unicode), _returns=Unicode, _in_variable_names={"Payload": "Payload"})
    def CreateDERGroups(ctx, header, payload, **kwarg):
        re = DERGroupsResponseMessageType
        # aa = helpers.serialize_object(header)
        # for i in header.gi_frame.f_locals['element']:
        #     print(i)
        # for i in payload:
        #     print(i)
        # print(kwarg)
        # print(ctx)
        # from pprint import pprint
        # pprint(header)  # ,  _in_header=xml,
        # pprint(payload)
        reply = ReplyType()
        error = False
        for i in payload.DERGroups.EndDeviceGroup:
            if not i.mRID:
                i.mRID = str(uuid.uuid4())
                re.Payload = payload
            # print(i)
            # print(i.DERFunction)
            # print(i.mRID)
            # print(i.description)
            # for ii in i.EndDevices:
            #     print(ii)
            # for ii in i.Names:
            #     print(ii)
            try:
                insertEndDeviceGroup(i)
            except SamemRIDException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.mRID, kind=IDKindType.UUID)
            except SameGroupNameException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.description, kind=IDKindType.NAME)

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

    @rpc(DERGroupsRequestMessageType, _returns=DERGroupsResponseMessageType)
    def DeleteDERGroups(ctx, request, **kwargs):
        groups = request.Payload.DERGroups.EndDeviceGroup
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
                    deleteDERGroupByName(name)
                except SameGroupNameException as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=name, kind=IDKindType.NAME)
            else:
                try:
                    deleteDERGroupByMrid(mrid)
                except SamemRIDException as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=mrid, kind=IDKindType.UUID)

        re = DERGroupsResponseMessageType
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


    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType)
    def ChangeDERGroups(ctx, header, paylaod, **kwargs):
        pass

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

getDevices = Application(
    services=[GetDevicesService],
    tns='der.pnnl.gov',
    name='GetDevicesService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())
createDERGroups = Application(
    services=[CreateDERGroupsService],
    tns='der.pnnl.gov',
    name='CreateDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
getDERGroups = Application(
    services=[GetDERGroupsService],
    tns='der.pnnl.gov',
    name='GetDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
executeDERGroups =  Application(
    services=[ExecuteDERGroupsService],
    tns='der.pnnl.gov',
    name='ExecuteDERGroupsService',
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
    'getDERGroups': getDERGroups,
})

wsgi_app = WsgiMounter({
    'get': wsgi_app_get_sub,
    'create': WsgiMounter({'executeDERGroups': createDERGroups}),
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
    logging.info("GetDevicesService wsdl is at: http://localhost:8008/get/getDevices?wsdl")
    logging.info("GetDERGroupsService wsdl is at: http://localhost:8008/get/getDERGroups?wsdl")
    logging.info("CreateDERGroupsService wsdl is at: http://localhost:8008/create/executeDERGroups?wsdl")
    logging.info("ExecuteDERGroupsService wsdl is at: http://localhost:8008/change/executeDERGroups?wsdl")


    server = make_server('127.0.0.1', 8008, wsgi_app)
    server.serve_forever()
