from DERGroups import DERGroups
from message import OperationSet, ReplyType, RequestType, HeaderType
from spyne import ComplexModel, Unicode


class DERGroupsPayloadType(ComplexModel):
    _type_info = [
        ('DERGroups', DERGroups),
        ('OperationSet', OperationSet),
        ('Compressed', Unicode),
        ('Format', Unicode)
    ]

    def __init__(self, DERGroups=None, operationSet=None, compressed=None, format=None, **kwargs):
        super().__init__(DERGroups, operationSet, compressed, format, **kwargs)
        self.DERGroups = DERGroups
        self.operationSet = operationSet
        self.compressed = compressed
        self.format = format
# end class DERGroupsPayloadType


class DERGroupsRequestMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Request', RequestType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, request=None, payload=None, **kwargs):
        super().__init__(header, request, payload, **kwargs)
        self.header = header
        self.request = request
        self.payload = payload
# end class DERGroupsRequestMessageType


class DERGroupsResponseMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(header, reply, payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class DERGroupsResponseMessageType


class DERGroupsEventMessageType(ComplexModel):
    _type_info = [
        ('Header', HeaderType),
        ('Payload', DERGroupsPayloadType),
    ]

    def __init__(self, header=None, payload=None, **kwargs):
        super().__init__(header, payload, **kwargs)
        self.header = header
        self.payload = payload
# end class DERGroupsEventMessageType


class DERGroupsFaultMessageType(ComplexModel):
    _type_info = [
        ('Reply', ReplyType),
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(reply, **kwargs)
        self.reply = reply
# end class DERGroupsFaultMessageType