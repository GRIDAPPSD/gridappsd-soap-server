from message import HeaderType
from message import OperationSet
from message import ReplyType
from message import RequestType
from spyne import ComplexModel, Unicode


class DERGroupsPayloadType(ComplexModel):
    _type_info = [
        ('OperationSet', OperationSet),
        ('Compressed', Unicode),
        ('Format', Unicode),
    ]

    def __init__(self, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(OperationSet=operationSet, Compressed=compressed, Format=format, **kwargs)
        self.operationSet = operationSet
        self.compressed = compressed
        self.format = format
# end class DERGroupsPayloadType


class DERGroupsOperationSetRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', RequestType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, request=None, payload=None, **kwargs):
        super().__init__(Header=header, Request=request, Payload=payload, **kwargs)
        self.header = header
        self.request = request
        self.payload = payload
# end class DERGroupsOperationSetRequestMessageType


class DERGroupsOperationSetResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupsOperationSetResponseMessageType


class DERGroupsOperationSetEventMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, payload=None, **kwargs):
        super().__init__(Header=header, Payload=payload, **kwargs)
        self.header = header
        self.payload = payload
# end class DERGroupsOperationSetEventMessageType


class DERGroupsOperationSetFaultMessageType(ComplexModel):
    _type_info = [
        ('Reply', ReplyType),
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(Reply=reply, **kwargs)
        self.reply = reply
# end class DERGroupsOperationSetFaultMessageType