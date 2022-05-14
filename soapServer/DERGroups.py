from spyne import ComplexModel, Unicode, Integer, Uuid, Array, DateTime, Boolean, Decimal, XmlAttribute, XmlData
from message import Name
import datetime as datetime_


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

    def __init__(self, connectDisconnect=None, frequencyWattCurveFunction=None, maxRealPowerLimiting=None,
                 rampRateControl=None, reactivePowerDispatch=None, realPowerDispatch=None, voltageRegulation=None,
                 voltVarCurveFunction=None, voltWattCurveFunction=None, **kwargs):
        super().__init__(connectDisconnect=connectDisconnect,
                         frequencyWattCurveFunction=frequencyWattCurveFunction,
                         maxRealPowerLimiting=maxRealPowerLimiting,
                         rampRateControl=rampRateControl,
                         reactivePowerDispatch=reactivePowerDispatch,
                         realPowerDispatch=realPowerDispatch,
                         voltageRegulation=voltageRegulation,
                         voltVarCurveFunction=voltVarCurveFunction,
                         voltWattCurveFunction=voltWattCurveFunction, **kwargs)
        self.connectDisconnect = connectDisconnect
        self.frequencyWattCurveFunction = frequencyWattCurveFunction
        self.maxRealPowerLimiting = maxRealPowerLimiting
        self.rampRateControl = rampRateControl
        self.reactivePowerDispatch = reactivePowerDispatch
        self.realPowerDispatch = realPowerDispatch
        self.voltageRegulation = voltageRegulation
        self.voltVarCurveFunction = voltVarCurveFunction
        self.voltWattCurveFunction = voltWattCurveFunction


class Version(ComplexModel):
    """This is the version for a group of devices or objects. This could be
    used to track the version for any group of objects or devices over
    time. For example, for a DERGroup, the requesting system may want to
    get the details of a specific version of a DERGroup."""
    _type_info = [
        ('date', DateTime),
        ('major', Integer),
        ('minor', Integer),
        ('revision', Integer),
    ]

    def __init__(self, date=None, major=None, minor=None, revision=None, **kwargs):
        super().__init__(date=None, major=None, minor=None, revision=None, **kwargs)
        if isinstance(date, str):
            initvalue_ = datetime_.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = date
        self.date = initvalue_
        self.major = major
        self.minor = minor
        self.revision = revision


class EndDevice(ComplexModel):
    """Asset container that performs one or more end device functions. One type
    of end device is a meter which can perform metering, load management,
    connect/disconnect, accounting functions, etc. Some end devices, such
    as ones monitoring and controlling air conditioners, refrigerators,
    pool pumps may be connected to a meter. All end devices may have
    communication capability defined by the associated communication
    function(s). An end device may be owned by a consumer, a service
    provider, utility or otherwise.There may be a related end device
    function that identifies a sensor or control point within a metering
    application or communications systems (e.g., water, gas,
    electricity).Some devices may use an optical port that conforms to the
    ANSI C12.18 standard for communications."""
    __type_name__ = 'mRID'
    _type_info = [
        ('mRID', Uuid),  # XmlData(Uuid)
        ('Names', Name.customize(max_occurs="unbounded", min_occurs=0))
    ]

    def __init__(self, mRID=None, names=None, **kwargs):
        super().__init__(mRID=mRID, Names=names, **kwargs)
        self.mRID = mRID
        if names is None:
            self.names = []
        else:
            self.names = names


# class NameType(ComplexModel):
#     __type_name__ = 'name'
#     _type_info = [
#         ('name', Unicode)
#     ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


class EndDeviceGroup(ComplexModel):
    """Abstraction for management of group communications within a two-way AMR
    system or the data for a group of related end devices. Commands can be
    issued to all of the end devices that belong to the group using a
    defined group address and the underlying AMR communication
    infrastructure. A DERGroup and a PANDeviceGroup is an
    EndDeviceGroup."""
    _type_info = [
        ('mRID', Unicode),
        ('description', Unicode),
        ('DERFunction', DERFunction),
        ('EndDevices', EndDevice.customize(max_occurs="unbounded", min_occurs=0)),
        ('Names', Name.customize(max_occurs="unbounded", min_occurs=0)),
        ('version', Version),
    ]

    def __init__(self, mRID=None, description=None, DERFunction=None, endDevices=None, names=None, version=None, **kwargs):
        super().__init__(mRID=mRID, description=description, DERFunction=DERFunction, EndDevices=endDevices, Names=names, version=version, **kwargs)
        self.mRID = mRID
        self.description = description
        self.DERFunction = DERFunction
        if endDevices is None:
            self.endDevices = []
        else:
            self.endDevices = endDevices
        if names is None:
            self.names = []
        else:
            self.names = names
        self.version = version


class DERGroups(ComplexModel):
    _type_info = [
        # ('DERGroups', Array(EndDeviceGroup)),
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs="unbounded", min_occurs=1)),
    ]

    def __init__(self, endDeviceGroup=None, **kwargs):
        super().__init__(EndDeviceGroup=endDeviceGroup, **kwargs)
        if endDeviceGroup is None:
            self.endDeviceGroup = []
        else:
            self.endDeviceGroup = endDeviceGroup
