import datetime as datetime_
from spyne import ComplexModel, Unicode, DateTime, AnyDict

from DERGroupForecastQueries import DERGroupForecastQueries
from DERGroupForecasts import DERGroupForecasts
from message import HeaderType
from message import OperationSet
from message import OptionType
from message import ReplyType


class DERGroupForecastQueriesRequestType(ComplexModel):
    """ -- This can be a CIM profile defined as an XSD with a CIM-specific namespace
    StartTime -- Start time of interest
    EndTime -- End time of interest
    Option -- Request type specialization
    ID -- Object ID for request

    """
    _type_info = [
        ('StartTime', DateTime.customize(min_occurs=0)),
        ('EndTime', DateTime.customize(min_occurs=0)),
        ('Option', OptionType.customize(max_occurs='unbounded', min_occurs=0)),
        ('ID', Unicode.customize(max_occurs='unbounded', min_occurs=0)),
        ('DERGroupForecastQueries', DERGroupForecastQueries),
        ('__ANY__', AnyDict)
    ]

    def __init__(self, startTime=None, endTime=None, option=None, id=None, dERGroupForecastQueries=None, **kwargs):
        super().__init__(StartTime=startTime, EndTime=endTime, Option=option, ID=id, DERGroupStatusQueries=dERGroupForecastQueries, **kwargs)
        if isinstance(startTime, str):
            initvalue_ = datetime_.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = startTime
        self.StartTime = initvalue_
        if isinstance(endTime, str):
            initvalue_ = datetime_.datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = endTime
        self.EndTime = initvalue_
        if option is None:
            self.Option = []
        else:
            self.Option = option
        if id is None:
            self.ID = []
        else:
            self.ID = id
        self.DERGroupForecastQueries = dERGroupForecastQueries
        # if anytypeobjs_ is None:
        #     self.anytypeobjs_ = []
        # else:
        #     self.anytypeobjs_ = anytypeobjs_
# end class DERGroupForecastQueriesRequestType


class DERGroupForecastQueriesRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', DERGroupForecastQueriesRequestType.customize(min_occurs=0))
    ]
    def __init__(self, header=None, request=None, **kwargs):
        super().__init__(Header=header, Request=request, **kwargs)
        self.Header = header
        self.Request = request
# end class DERGroupForecastQueriesRequestMessageType


class DERGroupForecastQueriesPayloadType(ComplexModel):
    """Compressed -- For compressed and/or binary, uuencoded payloads
    Format -- Hint as to format of payload, e.g. XML, RDF, SVF, BINARY, PDF, ...

    """
    _type_info = [
        ('DERGroupStatuses', DERGroupForecasts.customize(min_occurs=0)),
        ('OperationSet', OperationSet.customize(min_occurs=0)),
        ('Compressed', Unicode.customize(min_occurs=0)),
        ('Format', Unicode.customize(min_occurs=0))
    ]

    def __init__(self, dERGroupForecasts=None, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(DERGroupStatuses=dERGroupForecasts, OperationSet=operationSet, Compressed=compressed, Format=format, **kwargs)
        self.DERGroupForecasts = dERGroupForecasts
        self.OperationSet = operationSet
        self.Compressed = compressed
        self.Format = format
# end class DERGroupForecastQueriesPayloadType


class DERGroupForecastQueriesResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupForecastQueriesPayloadType.customize(min_occurs=0))
    ]
    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.Header = header
        self.Reply = reply
        self.Payload = payload
# end class DERGroupForecastQueriesResponseMessageType


class DERGroupForecastQueriesFaultMessageType(ComplexModel):
    _type_info = [
        ('Reply', ReplyType)
    ]
    def __init__(self, reply=None, **kwargs):
        super().__init__(Reply=reply, **kwargs)
        self.Reply = reply
# end class DERGroupForecastQueriesFaultMessageType


class DERGroupForecastQueriesResponseType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupForecastQueriesPayloadType.customize(min_occurs=0))
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.Header = header
        self.Reply = reply
        self.Payload = payload
# end class DERGroupForecastQueriesResponseType
