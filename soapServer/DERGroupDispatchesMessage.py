from DERGroupDispatches import DERGroupDispatches
from message import OperationSet, ReplyType, RequestType, HeaderType
from spyne import ComplexModel, Unicode

class DERGroupDispatchesPayloadType(ComplexModel):
    _type_info = [
        ('DERGroupDispatches', DERGroupDispatches),
        ('OperationSet', OperationSet),
        ('Compressed', Unicode),
        ('Format', Unicode)
    ]

    def __init__(self, DERGroupDispatches=None, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(DERGroupDispatches=DERGroupDispatches, OperationSet=operationSet, Compressed=compressed, Format=format, **kwargs)
        self.DERGroupDispatches = DERGroupDispatches
        self.operationSet = operationSet
        self.compressed = compressed
        self.format = format


class DERGroupDispatchesRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', RequestType),
        ('Payload', DERGroupDispatchesPayloadType),
    ]

    def __init__(self, header=None, request=None, payload=None, **kwargs):
        super().__init__(Header=header, Request=request, Payload=payload, **kwargs)
        self.header = header
        self.request = request
        self.payload = payload


class DERGroupDispatchesResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupDispatchesPayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(Header=header, Reply=reply, Payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload


class DERGroupDispatchesEventMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Payload', DERGroupDispatchesPayloadType),
    ]

    def __init__(self, header=None, payload=None, **kwargs):
        super().__init__(Header=header, Payload=payload, **kwargs)
        self.header = header
        self.payload = payload


class DERGroupDispatchesFaultMessageType(ComplexModel):
    _type_info = [
        ('Reply', ReplyType),
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(Reply=reply, **kwargs)
        self.reply = reply