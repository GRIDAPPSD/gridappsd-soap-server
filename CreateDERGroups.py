from spyne import ComplexModel, Unicode, Integer, Uuid, Array, DateTime, Boolean, Decimal, XmlAttribute, XmlData



class Header(ComplexModel):
    _type_info = [
        ('Verb', Unicode),
        ('Noun', Unicode),
        ('Timestamp', DateTime),
        ('MessageID', Uuid),
        ('CorrelationID', Uuid),
    ]

    def __init__(self):
        super().__init__()


class DERFunction(ComplexModel):
    _type_info = [
        ('connectDisconnect', Boolean),
        ('frequencyWattCurveFunction', Boolean),
        ('maxRealPowerLimiting', Boolean),
        ('rampRateControl', Boolean),
        ('reactivePowerDispatch', Boolean),
        ('realPowerDispatch', Boolean),
        ('voltageRegulation', Boolean),
        ('voltVarCurveFunction', Boolean),
        ('voltWattCurveFunction', Boolean),
    ]

    def __init__(self):
        super().__init__()


class Version(ComplexModel):
    _type_info = [
        ('date', DateTime),
        ('major', Integer),
        ('minor', Integer),
        ('revision', Integer),
    ]

    def __init__(self):
        super().__init__()


class EndDeviceType(ComplexModel):
    __type_name__ = 'mRID'
    _type_info = [
        ('mRID', Uuid)#XmlData(Uuid)
    ]

    def __init__(self):
        super().__init__()


class nameType(ComplexModel):
    __type_name__ = 'name'
    _type_info = [
        ('name', Unicode)
    ]

    def __init__(self):
        super().__init__()


class EndDeviceGroup(ComplexModel):
    _type_info = [
        ('mRID', Uuid),
        ('description', Unicode),
        ('DERFunction', DERFunction),
        ('EndDevices', EndDeviceType.customize(max_occurs="unbounded")),
        ('Names', nameType.customize(max_occurs="unbounded")),
        ('version', Version),
    ]

    def __init__(self):
        super().__init__()


class Payload(ComplexModel):
    _type_info = [
        ('DERGroups', Array(EndDeviceGroup)),
    ]

    def __init__(self):
        super().__init__()


class DERGroupsMessage(ComplexModel):
    _type_info = [
        ('Header', Header),
        ('Payload', Payload),
    ]

    def __init__(self):
        super().__init__()


class UUIDWithAttribute(ComplexModel):
    __type_name__ = 'ID'
    _type_info = [
        ('kind', XmlAttribute(Unicode)),
        ('objectType', XmlAttribute(Unicode)),
        ('value', XmlData(Uuid)),
    ]

    # def __init__(self):
    #     super().__init__()

    def __init__(self, kind, objectType, uuid):
        super().__init__()
        self.kind = kind
        self.objectType = objectType
        self.value = uuid


class Error(ComplexModel):
    _type_info = [
        ('code', Decimal),
        ('level', Unicode),
        ('reason', Unicode),
        ('ID', UUIDWithAttribute),
    ]

    def __init__(self, code, level, reason, ID):
        super().__init__()
        self.code = code
        self.level = level
        self.reason = reason
        self.ID = ID


class Reply(ComplexModel):
    _type_info = [
        ('Result', Unicode),
        ('Error', Error),
    ]

    def __init__(self, result='OK', error=None):
        super().__init__()
        self.Result = result
        self.Error = error


class ResponseMessage(ComplexModel):
    _type_info = [
        ('Header', Header),
        ('Reply', Reply),
    ]

    def __init__(self):
        super().__init__()
