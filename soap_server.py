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
from device import Devices, SynchronousMachine, Solar, Battery
from CreateDERGroups import DERGroupsMessage, Payload, Header, Reply, ResponseMessage, Error, UUIDWithAttribute

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

    @rpc(_returns=Devices)
    def GetDevices(ctx):
        synchronousMachine = conn.query_data(Queries.querySynchronousMachine)
        solar = conn.query_data(Queries.querySolar)
        battery = conn.query_data(Queries.queryBattery)
        syndeviceList = []
        slrdeviceList = []
        bttrydeviceList = []
        for r in synchronousMachine['data']['results']['bindings']:
            d = SynchronousMachine(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
            syndeviceList.append(d)
        for r in solar['data']['results']['bindings']:
            d = Solar(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
            slrdeviceList.append(d)
        for r in battery['data']['results']['bindings']:
            d = Battery(r['name']['value'], r['bus']['value'], r['ratedS']['value'], r['ratedU']['value'], r['ipu']['value'], r['ratedE']['value'], r['storedE']['value'], r['state']['value'], r['p']['value'], r['q']['value'], r['id']['value'], r['fdrid']['value'], r['phases']['value'])
            bttrydeviceList.append(d)
        # pprint.pprint(results)
        # print(type(results))
        # print(len(results))
        # r = util.etreeconv.root_dict_to_etree({'r':results})
        # print(r)
        # return util.etreeconv.root_dict_to_etree({'a': 1})
        # return {'SynchronousMachine': synchronousMachine, 'Solar': solar, 'Battery': battery}
        return Devices(syndeviceList, slrdeviceList, bttrydeviceList)
        # return synchronousMachine
        # return json.dumps(deviceList)
        # return [o.__dict__ for o in deviceList]
        # s = {v.name: v.__dict__ for v in deviceList}
        # return {v.__class__.__name__: v.__dict__ for v in deviceList}


class CreateDERGroupsService(ServiceBase):
    # __in_header__ = Header
    # __port_types__ = ['ExecuteDERGroupsPort1']

    @rpc(Header, Payload, _returns=ResponseMessage, _in_variable_names={"Payload": "Payload"})
    # @rpc(Iterable(Unicode), Iterable(Unicode), _returns=Unicode, _in_variable_names={"Payload": "Payload"})
    def CreateDERGroups(ctx, header, payload, **kwarg):
        # aa = helpers.serialize_object(header)
        # for i in header.gi_frame.f_locals['element']:
        #     print(i)
        # for i in payload:
        #     print(i)
        # print(kwarg)
        print(ctx)
        from pprint import pprint
        pprint(header)#,  _in_header=xml,
        pprint(payload)
        for i in payload.DERGroups:
            print(i)
            print(i.DERFunction)
            print(i.mRID)
            print(i.description)
            for ii in i.EndDevices:
                print(ii)
            for ii in i.Names:
                print(ii)


        re = ResponseMessage
        re.Header = header
        # respond with error
        # id = UUIDWithAttribute('uuid', 'DERGroups', uuid.uuid4())
        # er = Error(6.1, 'FATAL', 'Request cancelled per business rule', id)
        # re.Reply = Reply('Failed', er)
        # respond with OK
        re.Reply = Reply()
        return re


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
intr = getDevices.interface
imports = intr.imports

print('imports: ', imports)
tns = getDevices.interface.get_tns()
print('tns: ', tns)
smm = getDevices.interface.service_method_map
print('smm: ', smm)
print(smm['{%s}GetDevices' % tns][0].service_class)
print(smm['{%s}GetDevices' % tns][0].service_class == GetDevicesService)
print(smm['{%s}GetDevices' % tns][0].function)
print(smm['{%s}GetDevices' % tns][0].function == GetDevicesService.GetDevices)
from spyne.interface.wsdl import Wsdl11
wsdl = Wsdl11(intr)
wsdl.build_interface_document('URL')
wsdl_str = wsdl.get_interface_document()
pprint.pprint(wsdl_str)
wsdl_doc = etree.fromstring(wsdl_str)
pprint.pprint('wsdl_doc')
pprint.pprint(wsdl_doc)

imports2 = createDERGroups.interface.imports
print('imports2: ', imports2)
tns2 = createDERGroups.interface.get_tns()
print('tns2: ', tns2)
smm2 = createDERGroups.interface.service_method_map
print('smm2: ', smm2)
print(smm2['{%s}CreateDERGroups' % tns2][0].service_class)
print(smm2['{%s}CreateDERGroups' % tns2][0].function)

RequestStatus = Unicode(values=['new', 'processed'], zonta='bonta')


class DataRequest(ComplexModel):
    status = Array(RequestStatus)


class HelloWorldService(Service):
    @rpc(DataRequest)
    def some_call(ctx, dgrntcl):
        pass


hw = Application([HelloWorldService], 'spyne.examples.hello.soap',
            in_protocol=Soap11(validator='lxml'),
            out_protocol=Soap11())

from spyne.util.xml import get_schema_documents
docs = get_schema_documents([ResponseMessage])
print(docs)
doc = docs['tns']
print(doc)
pprint.pprint(etree.tostring(doc, pretty_print=True))

print(ResponseMessage.resolve_namespace(ResponseMessage, __name__))

wsgi_app = WsgiMounter({
    'getDevices': getDevices,
    'createDERGroups': createDERGroups,
    'hw': hw
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
    logging.info("GetDevicesService wsdl is at: http://localhost:8008/getDevices?wsdl")
    logging.info("CreateDERGroupsService wsdl is at: http://localhost:8008/createDERGroups?wsdl")

    server = make_server('127.0.0.1', 8008, wsgi_app)
    server.serve_forever()
