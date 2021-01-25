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

from spyne import Application, Service, ComplexModel, rpc, ServiceBase, Iterable, Integer, Unicode, util, xml, AnyXml, \
    Array, AnyDict

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter
from gridappsd import GridAPPSD
from gridappsd import topics as t

from device import Device
from equipment import Equipments, SynchronousMachine, Solar, Battery
from DERGroups import DERGroups, EndDeviceGroup, EndDevice, DERFunction
from exceptions import SamemRIDException, SameGroupNameException
from message import ReplyType, HeaderType, ResultType, ErrorType, LevelType, UUIDWithAttribute, VerbType, IDKindType, \
    Name
from ExecuteDERGroupsCommands import insertEndDeviceGroup, deleteDERGroupByMrid, deleteDERGroupByName, modifyDERGroup
from DERGroupsMessage import DERGroupsPayloadType, DERGroupsResponseMessageType, DERGroupsRequestMessageType
from datetime import datetime
from DERGroupQueries import DERGroupQueries
from DERGroupQueriesMessage import DERGroupQueriesResponseMessageType, DERGroupQueriesRequestType, \
    DERGroupQueriesPayloadType
from DERGroupStatusQueriesMessage import DERGroupStatusQueriesResponseMessageType, DERGroupStatusQueriesRequestType

conn = GridAPPSD()
# conn.subscribe()

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


def _build_response_header(verb):
    '''
    create message header
    :param verb: string. create, change, delete execute, get , reply, etc.
    :param message_id: string. UUID
    :param correlation_id: string. UUID
    :return: json string as the header
    '''

    return HeaderType(verb=verb, noun="DERGroups", timestamp=datetime.now(), messageID=uuid.uuid4(),
                      correlationID=uuid.uuid4())


def _build_reply(result, errorCode, errorLevel=None, reason=None):
    reply = ReplyType()
    reply.Result = result
    if errorLevel:
        reply.Error = ErrorType(code=errorCode)
    else:
        reply.Error = ErrorType(code=errorCode, level=errorLevel, reason=reason)
    return reply


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
            dd = Device(name=d['name']['value'], mRID=d['mrid']['value'], isSmartInverter=smart,
                        usagePoint=d['upoint']['value'])
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


# class GetDERGroupsService(ServiceBase):
#
#     @rpc(_returns=DERGroups)
#     def GetDERGroups(ctx):
#         createdDERGroups = conn.query_data(Queries.queryAllDERGroups)
#         print(createdDERGroups)
#         groups = []
#         for g in createdDERGroups['data']['results']['bindings']:
#             mRID = g['mRID']['value']
#             description = None
#             if 'description' in g:
#                 description = g['description']['value']
#             name = g['names']['value']
#             d = g['devices']['value']
#             endDevices = []
#             if d:
#                 ds = d.split('\n')
#                 for dd in ds:
#                     ids = dd.split(',')
#                     # edNames=[]
#                     # edNames.append(Name(name=ids[1]))
#                     endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
#                 print(ds)
#             names = []
#             if name:
#                 nm = name.split('\n')
#                 for nn in nm:
#                     names.append(Name(name=nn))
#             f = g['funcs']['value']
#             funcs = dict()
#             if f:
#                 fs = f.split('\n')
#                 for ff in fs:
#                     func = ff.split(',')
#                     if func[1] == 'true':
#                         funcs[func[0]] = True
#                     else:
#                         funcs[func[0]] = False
#                 derfunc = DERFunction(connectDisconnect=funcs['connectDisconnect'],
#                                       frequencyWattCurveFunction=funcs['frequencyWattCurveFunction'],
#                                       maxRealPowerLimiting=funcs['maxRealPowerLimiting'],
#                                       rampRateControl=funcs['rampRateControl'],
#                                       reactivePowerDispatch=funcs['reactivePowerDispatch'],
#                                       realPowerDispatch=funcs['realPowerDispatch'],
#                                       voltageRegulation=funcs['voltageRegulation'],
#                                       voltVarCurveFunction=funcs['voltVarCurveFunction'],
#                                       voltWattCurveFunction=funcs['voltWattCurveFunction'])
#             newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=names,
#                                       DERFunction=derfunc)
#             groups.append(newgroup)
#         if groups:
#             return DERGroups(endDeviceGroup=groups)
#         else:
#             return DERGroups(endDeviceGroup=None)


class CreateDERGroupsService(ServiceBase):
    # __in_header__ = Header
    # __port_types__ = ['ExecuteDERGroupsPort1']

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType,
         _in_variable_names={"Payload": "Payload"})
    # @rpc(Iterable(Unicode), Iterable(Unicode), _returns=Unicode, _in_variable_names={"Payload": "Payload"})
    def CreateDERGroups(ctx, Header=None, Payload=None, **kwarg):
        re = DERGroupsResponseMessageType
        reply = ReplyType()
        error = False
        for i in Payload.DERGroups.EndDeviceGroup:
            if not i.mRID:
                i.mRID = str(uuid.uuid4())
                re.Payload = Payload
            try:
                insertEndDeviceGroup(i)
            except SamemRIDException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.mRID, kind=IDKindType.UUID)
            except SameGroupNameException:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup", value=i.description, kind=IDKindType.NAME)
            except Exception as ex:
                error = True
                eid = UUIDWithAttribute(objectType="DERGroup")
                print(ex)

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

    @rpc(HeaderType, DERGroupsPayloadType, _returns=DERGroupsResponseMessageType)
    def DeleteDERGroups(ctx, Header=None, Payload=None, **kwargs):
        groups = Payload.DERGroups.EndDeviceGroup
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
                    deleteDERGroupByName(name.name)
                except Exception as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=name, kind=IDKindType.NAME)
            else:
                try:
                    deleteDERGroupByMrid(mrid)
                except SamemRIDException as ex:
                    error = True
                    eid = UUIDWithAttribute(objectType="DERGroup", value=mrid, kind=IDKindType.UUID)

        re = DERGroupsResponseMessageType
        re.Header = _build_response_header(VerbType.REPLY)
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
    def ChangeDERGroups(ctx, Header=None, Payload=None, **kwargs):
        print(Header)
        print(Payload)
        error = False
        reply = ReplyType()

        if Payload.DERGroups.EndDeviceGroup:
            group = Payload.DERGroups.EndDeviceGroup[0]

        try:
            modifyDERGroup(group)
        except Exception as ex:
            error = True
            # eid = UUIDWithAttribute(objectType="DERGroup")

        re = DERGroupsResponseMessageType
        re.Header = _build_response_header(VerbType.REPLY)

        if not error:
            reply.Result = ResultType.OK
            reply.Error = ErrorType(code='0.0')
        else:
            reply.Result = ResultType.FAILED
            reply.Error = ErrorType(code='6.1', level=LevelType.FATAL, reason='Request cancelled per business rule')
        re.Reply = reply
        return re


class QueryDERGroupsService(ServiceBase):
    @rpc(HeaderType, DERGroupQueriesRequestType, _returns=DERGroupQueriesResponseMessageType)
    def QueryDERGroups(ctx, Header=None, Request=None, **kwargs):
        print(Header)
        print(Request)
        names = []
        mRIDs = []
        if Request.DERGroupQueries.EndDeviceGroup:
            for group in Request.DERGroupQueries.EndDeviceGroup:
                if group:
                    if group.Names:
                        for name in group.Names:
                            names.append(name.name)
                            print(name.name)
                    elif group.mRID:
                        mRIDs.append(str(group.mRID))
                        print(group.mRID)
        if names:
            # b = "\"" + "\" \"".join(names) + "\""
            query = Queries.queryDERGroupsByName.format(groupnames="\"" + "\" \"".join(names) + "\"")
        if mRIDs:
            query = Queries.queryDERGroupsBymRID.format(mRIDs="\"" + "\" \"".join(mRIDs) + "\"")
        if not names and not mRIDs:
            query = Queries.queryAllDERGroups
        success = False
        try:
            groups = conn.query_data(query)
            success = True
        except Exception as e:
            pass
        re = DERGroupQueriesResponseMessageType
        reheader = _build_response_header(VerbType.REPLY)
        re.Header = reheader
        if success:
            payload = QueryDERGroupsService.build_response_payload(groups)
            reply = _build_reply(ResultType.OK, '0.0')
        else:
            payload = None
            reply = _build_reply(ResultType.FAILED, '6.1')
        re.Payload = payload
        re.Reply = reply
        return re

    @staticmethod
    def build_response_payload(groups):
        endgroups = []
        for g in groups['data']['results']['bindings']:
            mRID = None
            if 'mRID' in g:
                mRID = g['mRID']['value']
            description = None
            if 'description' in g:
                description = g['description']['value']
            names = g['names']['value']
            name = []
            if names:
                nms = names.split('\n')
                for nm in nms:
                    name.append(Name(name=nm))
            devices = g['devices']['value']
            endDevices = []
            if devices:
                dvcs = devices.split('\n')
                for dd in dvcs:
                    ids = dd.split(',')
                    endDevices.append(EndDevice(mRID=ids[0], names=[Name(name=ids[1])], isSmart=ids[2]))
            funcs = g['funcs']['value']
            derfuncs = dict()
            if funcs:
                fs = funcs.split('\n')
                for ff in fs:
                    func = ff.split(',')
                    if func[1] == 'true':
                        derfuncs[func[0]] = True
                    else:
                        derfuncs[func[0]] = False
                derfunc = DERFunction(connectDisconnect=derfuncs['connectDisconnect'],
                                      frequencyWattCurveFunction=derfuncs['frequencyWattCurveFunction'],
                                      maxRealPowerLimiting=derfuncs['maxRealPowerLimiting'],
                                      rampRateControl=derfuncs['rampRateControl'],
                                      reactivePowerDispatch=derfuncs['reactivePowerDispatch'],
                                      realPowerDispatch=derfuncs['realPowerDispatch'],
                                      voltageRegulation=derfuncs['voltageRegulation'],
                                      voltVarCurveFunction=derfuncs['voltVarCurveFunction'],
                                      voltWattCurveFunction=derfuncs['voltWattCurveFunction'])
            else:
                derfunc = None
            newgroup = EndDeviceGroup(mRID=mRID, description=description, endDevices=endDevices, names=name,
                                  DERFunction=derfunc)
            endgroups.append(newgroup)
        if endgroups:
            dergroups = DERGroups(endDeviceGroup=endgroups)
        else:
            dergroups = DERGroups(endDeviceGroup=None)

        re = DERGroupQueriesPayloadType(dERGroups=dergroups)
        return re


class QueryDERGroupStatusesService(ServiceBase):
    @rpc(HeaderType, DERGroupStatusQueriesRequestType, _returns=DERGroupStatusQueriesResponseMessageType)
    def QueryDERGroupStatuses(ctx, Header=None, Request=None, **kwargs):
        print(Header)
        print(Request)
        re = DERGroupStatusQueriesResponseMessageType
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
# getDERGroups = Application(
#     services=[GetDERGroupsService],
#     tns='der.pnnl.gov',
#     name='GetDERGroupsService',
#     in_protocol=Soap11(validator='lxml'),
#     out_protocol=Soap11()
# )
executeDERGroups = Application(
    services=[ExecuteDERGroupsService],
    tns='der.pnnl.gov',
    name='ExecuteDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
queryDERGroups = Application(
    services=[QueryDERGroupsService],
    tns='der.pnnl.gov',
    name='QueryDERGroupsService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
queryDERGroupStatuses = Application(
    services=[QueryDERGroupStatusesService],
    tns='der.pnnl.gov',
    name='QueryDERGroupStatusesService',
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
    # 'getDERGroups': getDERGroups,
    'queryDERGroups': queryDERGroups,
    'queryDERGroupStatuses': queryDERGroupStatuses
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
    # logging.info("GetDERGroupsService wsdl is at: http://localhost:8008/get/getDERGroups?wsdl")
    logging.info("CreateDERGroupsService wsdl is at: http://localhost:8008/create/executeDERGroups?wsdl")
    logging.info("ExecuteDERGroupsService wsdl is at: http://localhost:8008/change/executeDERGroups?wsdl")
    logging.info("QueryDERGroupsService wsdl is at: http://localhost:8008/get/queryDERGroups?wsdl")
    logging.info("QueryDERGroupStatusesService wsdl is at: http://localhost:8008/get/queryDERGroupStatuses?wsdl")

    server = make_server('127.0.0.1', 8008, wsgi_app)
    server.serve_forever()
