from spyne import ComplexModel, Enum, Unicode, DateTime, Uuid, Decimal, XmlAttribute, XmlData, Integer, QName, Boolean
from spyne import AnyDict
import datetime as datetime_



#
# The super-class for enum types
#

# try:
#     from enum import Enum
# except ImportError:
#     Enum = object


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


"""ID Kind Type"""
IDKindType = Enum('NAME', 'UUID', 'TRANSACTION', 'OTHER', type_name='IDKindType')

"""Reply code: OK, PARTIAL or FAILED"""
ResultType = Enum('OK', 'PARTIAL', 'FAILED', type_name='ResultType')

"""This enumerated list of verbs that can be used to form message types in
compliance with the IEC 61968 standard."""
VerbType = Enum('CANCEL', 'CANCELED', 'CHANGE', 'CHANGED', 'CREATE', 'CREATED', 'CLOSE', 'CLOSED', 'DELETE', 'DELETED', 'GET', 'REPLY', 'EXECUTE', 'EXECUTED', type_name='VerbType')

"""Severity level, e.g. INFORM, WARNING, FATAL, CATASTROPHIC"""
LevelType = Enum('INFORM', 'WARNING', 'FATAL', 'CATASTROPHIC', type_name='LevelType')


class UUIDWithAttribute(ComplexModel):
    __type_name__ = 'ID'
    _type_info = [
        ('idType', XmlAttribute(Unicode)),
        ('idAuthority', XmlAttribute(Unicode)),
        ('kind', XmlAttribute(IDKindType)),
        ('objectType', XmlAttribute(Unicode)),
        ('value', XmlData(Uuid)),
    ]

    # def __init__(self):
    #     super().__init__()

    def __init__(self, kind=None, objectType=None, value=None, idType=None, idAuthority=None, **kwargs):
        super().__init__(kind=kind, objectType=objectType, value=value, idType=idType, idAuthority=idAuthority, **kwargs)
        self.kind = kind
        self.objectType = objectType
        self.value = value
        self.idType = idType
        self.idAuthority = idAuthority


# class Error(ComplexModel):
#     _type_info = [
#         ('code', Unicode),
#         ('level', Unicode),
#         ('reason', Unicode),
#         ('ID', UUIDWithAttribute),
#     ]
#
#     def __init__(self, code, level, reason, ID):
#         super().__init__()
#         self.code = code
#         self.level = level
#         self.reason = reason
#         self.ID = ID


# class Reply(ComplexModel):
#     _type_info = [
#         ('Result', Unicode),
#         ('Error', Error),
#     ]
#
#     def __init__(self, result='OK', error=None):
#         super().__init__()
#         self.Result = result
#         self.Error = error


# class ResponseMessage(ComplexModel):
#     _type_info = [
#         ('Header', Header),
#         ('Reply', Reply),
#     ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


# class Payload(ComplexModel):
#     # __namespace__ = "payload"
#     _type_info = [
#         ('DERGroups', Array(EndDeviceGroup)),
#     ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


# class DERGroupsMessage(ComplexModel):
#     _type_info = [
#         ('Header', Header),
#         ('Payload', DERGroups),
#     ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


class LocationType(ComplexModel):
    """Process location where error was encountered"""
    _type_info = [
        ('node', Unicode),
        ('pipeline', Unicode),
        ('stage', Unicode),
    ]

    def __init__(self, node=None, pipeline=None, stage=None, **kwargs):
        super().__init__(node, pipeline, stage, **kwargs)
        self.node = node
        self.pipeline = pipeline
        self.stage = stage
# end class LocationType


class NameTypeAuthority(ComplexModel):
    """From CIM"""
    _type_info = [
        ('name', Unicode),
        ('description', Unicode),
    ]

    def __init__(self, name=None, description=None, **kwargs):
        super().__init__(name, description, **kwargs)
        self.name = name
        self.description = description
# end class NameTypeAuthority


class NameType(ComplexModel):
    """From CIM"""
    _type_info = [
        ('name', Unicode),
        ('description', Unicode),
        ('NameTypeAuthority', NameTypeAuthority),
    ]

    def __init__(self, name=None, description=None, nameTypeAuthority=None, **kwargs):
        super().__init__(name, description, nameTypeAuthority, **kwargs)
        self.name = name
        self.description = description
        self.nameTypeAuthority = nameTypeAuthority
# end class NameType


class Name(ComplexModel):
    """From CIM"""
    _type_info = [
        ('name', Unicode),
        ('NameType', NameType),
    ]

    def __init__(self, name=None, nameType=None, **kwargs):
        super().__init__(name=name, NameType=nameType, **kwargs)
        self.name = name
        self.NameType = nameType
# end class Name


class ObjectType(ComplexModel):
    """Used to identify an object of interest"""
    _type_info = [
        ('mRID', Uuid),
        ('Name', Name),
        ('objectType', Unicode),
    ]

    def __init__(self, mRID=None, name=None, objectType=None, **kwargs):
        super().__init__(mRID, name, objectType, **kwargs)
        self.mRID = mRID
        if name is None:
            self.name = []
        else:
            self.name = name
        self.objectType = objectType
# end class ObjectType


class ErrorType(ComplexModel):
    """Error Structure"""
    _type_info = [
        ('code', Unicode),
        ('level', LevelType),
        ('reason', Unicode),
        ('details', Unicode),
        ('xpath', QName),
        ('stackTrace', Unicode),
        ('Location', LocationType),
        ('ID', UUIDWithAttribute),
        ('relatedID', UUIDWithAttribute),
        ('object', ObjectType),
        ('operationId', Integer),
    ]

    def __init__(self, code=None, level=None, reason=None, details=None, xpath=None, stackTrace=None, location=None, ID=None, relatedID=None, object=None, operationId=None, **kwargs):
        super().__init__(code=code, level=level, reason=reason, details=details, xpath=xpath, stackTrace=stackTrace, Location=location, ID=ID, relatedID=relatedID, object=object, operationId=operationId, **kwargs)
        self.code = code
        self.level = level
        self.reason = reason
        self.details = details
        self.xpath = xpath
        self.stackTrace = stackTrace
        self.location = location
        self.ID = ID
        self.relatedID = relatedID
        self.object = object
        self.operationId = operationId
# end class ErrorType


class ReplayDetectionType(ComplexModel):
    """Used to detect and prevent replay attacks"""
    _type_info = [
        ('Nonce', Unicode),
        ('Created', DateTime),
    ]

    def __init__(self, nonce=None, created=None, **kwargs):
        super().__init__(nonce, created, **kwargs)
        self.nonce = nonce
        if isinstance(created, str):
            initvalue_ = datetime_.datetime.strptime(created, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = created
        self.created = initvalue_
        self.created = None
# end class ReplayDetectionType


class UserType(ComplexModel):
    """User type definition"""
    _type_info = [
        ('UserID', Unicode),
        ('Organization', Unicode),
    ]

    def __init__(self, userID=None, organization=None, **kwargs):
        super().__init__(userID, organization, **kwargs)
        self.userID = userID
        self.organization = organization
# end class UserType


class MessageProperty(ComplexModel):
    """Message properties can be used for extended routing and filtering"""
    _type_info = [
        ('Name', Unicode),
        ('Value', Unicode),
    ]

    def __init__(self, name=None, value=None, **kwargs):
        super().__init__(name, value, **kwargs)
        self.name = name
        self.value = value
# end class MessageProperty


class HeaderType(ComplexModel):
    """Message header type definitionMessage header contains control and
    descriptive information about the message."""
    _type_info = [
        ('Verb', VerbType),
        ('Noun', Unicode),
        ('Revision', Unicode),
        ('ReplayDetection', ReplayDetectionType),
        ('Context', Unicode),
        ('Timestamp', DateTime),
        ('Source', Unicode),
        ('AsyncReplyFlag', Boolean),
        ('ReplyAddress', Unicode),
        ('AckRequired', Boolean),
        ('User', UserType),
        ('MessageID', Uuid),
        ('CorrelationID', Uuid),
        ('Comment', Unicode),
        ('Property', MessageProperty),
        ('__ANY__', AnyDict)
    ]

    def __init__(self, verb=None, noun=None, revision=None, replayDetection=None, context=None, timestamp=None, source=None, asyncReplyFlag=None, replyAddress=None, ackRequired=None, user=None, messageID=None, correlationID=None, comment=None, property=None, anytypeobjs_=None, **kwargs):
        super().__init__(Verb=verb, Noun=noun, Revision=revision, ReplayDetection=replayDetection, Context=context, Timestamp=timestamp, Source=source, AsyncReplyFlag=asyncReplyFlag, ReplyAddress=replyAddress, AckRequired=ackRequired, User=user, MessageID=messageID, CorrelationID=correlationID, Comment=comment, Property=property, Anytypeobjs_=anytypeobjs_, **kwargs)
        self.verb = verb
        self.noun = noun
        self.revision = revision
        self.replayDetection = replayDetection
        self.context = context
        if isinstance(timestamp, str):
            initvalue_ = datetime_.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = timestamp
        self.timestamp = initvalue_
        self.source = source
        self.asyncReplyFlag = asyncReplyFlag
        self.replyAddress = replyAddress
        self.ackRequired = ackRequired
        self.user = user
        self.messageID = messageID
        self.correlationID = correlationID
        self.comment = comment
        if property is None:
            self.Property = []
        else:
            self.property = property
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
# end class HeaderType


class OperationType(ComplexModel):
    """For master data set synchronization XML payloads."""
    _type_info = [
        ('operationId', Integer),
        ('noun', Unicode),
        ('verb', VerbType),
        ('elementOperation', Boolean),
        ('__ANY__', AnyDict),
    ]

    def __init__(self, operationId=None, noun=None, verb=None, elementOperation=False, anytypeobjs_=None, **kwargs):
        super().__init__(operationId=operationId, noun=noun, verb=verb, elementOperation=elementOperation, anytypeobjs_=anytypeobjs_, **kwargs)
        self.operationId = operationId
        self.noun = noun
        self.verb = verb
        self.elementOperation = elementOperation
        self.anytypeobjs_ = anytypeobjs_
# end class OperationType


class OperationSet(ComplexModel):
    """Each operation set is a collection of operations that may require
    operational-integrity and/or sequence control."""
    _type_info = [
        ('enforceMsgSequence', Boolean),
        ('enforceTransactionalIntegrity', Boolean),
        ('Operation', OperationType),
    ]

    def __init__(self, enforceMsgSequence=None, enforceTransactionalIntegrity=None, operation=None, **kwargs):
        super().__init__(enforceMsgSequence, enforceTransactionalIntegrity, operation, **kwargs)
        self.enforceMsgSequence = enforceMsgSequence
        self.enforceTransactionalIntegrity = enforceTransactionalIntegrity
        if operation is None:
            self.operation = []
        else:
            self.operation = operation
# end class OperationSet


class PayloadType(ComplexModel):
    """Payload container"""
    _type_info = [
        ('__ANY__', AnyDict),
        ('OperationSet', OperationSet),
        ('Compressed', Unicode),
        ('ID', Unicode),
        ('Format', Unicode)
    ]

    def __init__(self, anytypeobjs_=None, operationSet=None, compressed=None, ID=None, format=None, **kwargs):
        super().__init__(anytypeobjs_, operationSet, compressed, ID, format, **kwargs)
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.operationSet = operationSet
        self.compressed = compressed
        if ID is None:
            self.ID = []
        else:
            self.ID = ID
        self.Format = format
# end class PayloadType


class EventMessageType(ComplexModel):
    """Event Message Type, which is used to indicate a condition of potential
    interest. Note that the Payload may be required in the future."""
    _type_info = [
        ('Header', HeaderType),
        ('Payload', PayloadType),
    ]

    def __init__(self, header=None, payload=None, **kwargs):
        super().__init__(header, payload, **kwargs)
        self.header = header
        self.payload = payload
# end class EventMessageType


class ReplyType(ComplexModel):
    """Reply type definitionReply package is used to confirm success or report
    errors"""
    _type_info = [
        ('Result', ResultType),
        ('Error', ErrorType),
        ('ID', UUIDWithAttribute),
        ('__ANY__', AnyDict),
        ('operationId', Integer),
    ]

    def __init__(self, result=None, error=None, ID=None, anytypeobjs_=None, operationId=None, **kwargs):
        super().__init__(Result=result, Error=error, ID=ID, anytypeobjs_=anytypeobjs_, operationId=operationId, **kwargs)
        self.result = result
        if error is None:
            self.error = []
        else:
            self.error = error
        if ID is None:
            self.ID = []
        else:
            self.ID = ID
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.operationId = operationId
# end class ReplyType


class FaultMessageType(ComplexModel):
    """Fault Message Type, which is used in cases where the incoming message
    (including the header) cannot be parsed"""
    _type_info = [
        ('Reply', ReplyType),
    ]

    def __init__(self, reply=None, **kwargs):
        super().__init__(reply, **kwargs)
        self.reply = reply
# end class FaultMessageType


class OptionType(ComplexModel):
    _type_info = [
        ('name', Unicode),
        ('value', Unicode),
    ]

    def __init__(self, name=None, value=None, **kwargs):
        super().__init__(name, value, **kwargs)
        self.name = name
        self.value = value
# end class OptionType


class RequestType(ComplexModel):
    """Request type definitionRequest package is typically used to supply
    parameters for 'get' requests"""
    _type_info = [
        ('StartTime', DateTime),
        ('EndTime', DateTime),
        ('Option', OptionType),
        ('ID', UUIDWithAttribute),
        ('__ANY__', AnyDict),
    ]

    def __init__(self, startTime=None, endTime=None, option=None, ID=None, anytypeobjs_=None, **kwargs):
        super().__init__(startTime, endTime, option, ID, anytypeobjs_, **kwargs)
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
        if ID is None:
            self.ID = []
        else:
            self.ID = ID
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
# end class RequestType


class MessageType(ComplexModel):
    """Generic Message Type"""
    _type_info = [
        ('Header', HeaderType),
        ('Request', RequestType),
        ('Reply', ReplyType),
        ('Payload', PayloadType),
    ]

    def __init__(self, header=None, request=None, reply=None, payload=None, **kwargs):
        super().__init__(header, request, reply, payload, **kwargs)
        self.header = header
        self.request = request
        self.reply = reply
        self.payload = payload
# end class MessageType


class RequestMessageType(ComplexModel):
    """Request Message Type, which will typically result in a ResponseMessage
    to be returned. This is typically used to initiate a transaction or a
    query request."""
    _type_info = [
        ('Header', HeaderType),
        ('Request', RequestType),
        ('Payload', PayloadType),
    ]

    def __init__(self, header=None, request=None, payload=None, **kwargs):
        super().__init__(header, request, payload, **kwargs)
        self.header = header
        self.request = request
        self.payload = payload
# end class RequestMessageType


class ResponseMessageType(ComplexModel):
    """Response MessageType, typically used to reply to a RequestMessage"""
    _type_info = [
        ('Header', HeaderType),
        ('Reply', ReplyType),
        ('Payload', PayloadType),
    ]

    def __init__(self, header=None, reply=None, payload=None, **kwargs):
        super().__init__(header=header, reply=reply, payload=payload, **kwargs)
        self.header = header
        self.reply = reply
        self.payload = payload
# end class ResponseMessageType