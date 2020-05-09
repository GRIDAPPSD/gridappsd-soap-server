from DERGroupStatusQueries import DERGroupStatusQueries
from DERGroupStatuses import DERGroupStatuses
from message import HeaderType, OperationSet, OptionType, ReplyType
from spyne import ComplexModel, Unicode, DateTime, AnyDict
import datetime as datetime_


class DERGroupStatusQueriesFaultMessageType(ComplexModel):
    _type_info = [
        ('Reply', ReplyType)
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(Reply=reply, **kwargs)
        self.reply = reply
# end class DERGroupStatusQueriesFaultMessageType


class DERGroupStatusQueriesRequestType(ComplexModel):
    _type_info = [
        ('StartTime', DateTime.customize(min_occurs=0)),
        ('EndTime', DateTime.customize(min_occurs=0)),
        ('Option', OptionType.customize(max_occurs='unbounded', min_occurs=0)),
        ('ID', Unicode.customize(max_occurs='unbounded', min_occurs=0)),
        ('DERGroupStatusQueries', DERGroupStatusQueries),
        ('__ANY__', AnyDict)
    ]

    def __init__(self, startTime=None, endTime=None, option=None, id=None, dERGroupStatusQueries=None, **kwargs):
        super().__init__(StartTime=startTime, EndTime=endTime, Option=option, ID=id, DERGroupStatusQueries=dERGroupStatusQueries, **kwargs)
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
        self.dERGroupStatusQueries = dERGroupStatusQueries
        # if anytypeobjs_ is None:
        #     self.anytypeobjs_ = []
        # else:
        #     self.anytypeobjs_ = anytypeobjs_
# end class DERGroupStatusQueriesRequestType


class DERGroupStatusQueriesRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', DERGroupStatusQueriesRequestType.customize(min_occurs=0))
    ]

    def __init__(self, header=None, request=None, **kwargs):
        super().__init__(Header=header, Request=request, **kwargs)
        self.header = header
        self.request = request
# end class DERGroupStatusQueriesRequestMessageType


class DERGroupStatusQueriesPayloadType(ComplexModel):
    _type_info = [
        ('DERGroupStatuses', DERGroupStatuses.customize(min_occurs=0)),
        ('OperationSet', OperationSet.customize(min_occurs=0)),
        ('Compressed', Unicode.customize(min_occurs=0)),
        ('Format', Unicode.customize(min_occurs=0))
    ]

    def __init__(self, dERGroupStatuses=None, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(DERGroupStatuses=dERGroupStatuses, OperationSet=operationSet, Compressed=compressed, Format=format, **kwargs)
        self.dERGroupStatuses = dERGroupStatuses
        self.operationSet = operationSet
        self.compressed = compressed
        self.format = format
# end class DERGroupStatusQueriesPayloadType


class DERGroupStatusQueriesResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupStatusQueriesPayloadType.customize(min_occurs=0))
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupStatusQueriesResponseMessageType


class DERGroupStatusQueriesResponseType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupStatusQueriesPayloadType.customize(min_occurs=0))
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupStatusQueriesResponseType