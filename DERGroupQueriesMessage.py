from DERGroupQueries import DERGroupQueries
from DERGroups import DERGroups
from message import HeaderType
from message import OperationSet
from message import OptionType
from message import ReplyType
from spyne import ComplexModel, Unicode, DateTime, AnyDict
import datetime as datetime_


class DERGroupQueriesRequestType(ComplexModel):
    _type_info = [
        ('StartTime', DateTime),
        ('EndTime', DateTime),
        ('Option', OptionType),
        ('ID', Unicode),
        ('DERGroupQueries', DERGroupQueries),
        ('__ANY__', AnyDict),
    ]

    def __init__(self, startTime=None, endTime=None, option=None, id=None, dERGroupQueries=None, anytypeobjs_=None, **kwargs):
        super().__init__(StartTime=startTime, EndTime=endTime, Option=option, ID=id, DERGroupQueries=dERGroupQueries, anytypeobjs_=anytypeobjs_, **kwargs)
        if isinstance(startTime, str):
            initvalue_ = datetime_.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = startTime
        self.startTime = initvalue_
        if isinstance(endTime, str):
            initvalue_ = datetime_.datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = endTime
        self.endTime = initvalue_
        if option is None:
            self.option = []
        else:
            self.option = option
        if id is None:
            self.id = []
        else:
            self.id = id
        self.dERGroupQueries = dERGroupQueries
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
# end class DERGroupQueriesRequestType


class DERGroupQueriesRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', DERGroupQueriesRequestType)
    ]

    def __init__(self, header=None, request=None, **kwargs):
        super().__init__(Header=header, Request=request, **kwargs)
        self.header = header
        self.request = request
# end class DERGroupQueriesRequestMessageType


class DERGroupQueriesPayloadType(ComplexModel):
    _type_info = [
        ('DERGroups', DERGroups),
        ('OperationSet', OperationSet),
        ('Compressed', Unicode),
        ('Format', Unicode),
    ]

    def __init__(self, dERGroups=None, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(DERGroups=dERGroups, OperationSet=operationSet, Compressed=compressed, Format=format, **kwargs)
        self.dERGroups = dERGroups
        self.operationSet = operationSet
        self.compressed = compressed
        self.format = format
# end class DERGroupQueriesPayloadType


class DERGroupQueriesResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupQueriesPayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupQueriesResponseMessageType


class DERGroupQueriesFaultMessageType(ComplexModel):
    _type_info = [
        ('reply', ReplyType),
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(Reply=reply, **kwargs)
        self.reply = reply
# end class DERGroupQueriesFaultMessageType


class DERGroupQueriesResponseType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupQueriesPayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupQueriesResponseType
