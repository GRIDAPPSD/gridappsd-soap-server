from spyne import ComplexModel, Unicode, Integer, Uuid, Array, DateTime, Boolean, Decimal, XmlAttribute, XmlData, Float
from message import Name
import datetime as datetime_


class DERCurveData(ComplexModel):
    _type_info = [
        ('intervalNumber', Integer),
        ('nominalYValue', Float)
    ]

    def __init__(self, intervalnumber=None, nominalyvalue=None, **kwargs):
        super().__init__(intervalNumber = intervalnumber, nominalYValue = nominalyvalue, **kwargs)
        self.intervalNumber = intervalnumber
        self.nominalYValue = nominalyvalue


class DispatchSchedule(ComplexModel):
    _type_info = [
        ('curveStyleKind', Unicode),
        ('startTime', DateTime),
        ('timeIntervalDuration', Integer),
        ('timeIntervalUnit', Unicode),
        ('DERCurveData', DERCurveData.customize(max_occurs="unbounded", min_occurs=1))
    ]

    def __init__(self, curvestylekind=None, starttime=None, timeintervalduration=None, timeintervalunit=None, dercurvedata = None, **kwargs):
        super().__init__(curveStyleKind = curvestylekind, startTime = starttime, timeIntervalDuration = timeintervalduration, timeIntervalUnit = timeintervalunit, DERCurveData = dercurvedata, **kwargs)
        self.curveStyleKind = curvestylekind
        if isinstance(starttime, str):
            initvalue_ = datetime_.datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S%z')
        else:
            initvalue_ = starttime
        self.startTime = initvalue_
        self.timeIntervalDuration =timeintervalduration
        self.timeIntervalUnit = timeintervalunit
        if dercurvedata is None:
            self.DERCurveData = []
        else:
            self.DERCurveData = dercurvedata


class DERMonitorableParameter(ComplexModel):
    _type_info = [
        ('DERParameter', Unicode),
        ('flowDirection', Unicode),
        ('yMultiplier', Unicode),
        ('yUnit', Unicode),
        ('DispatchSchedule', DispatchSchedule.customize(max_occurs="unbounded", min_occurs=1))
    ]

    def __init__(self, derparameter=None, flowdirection=None, ymultiplier=None, yunit=None, dispatchschedule = None, **kwargs):
        super().__init__(DERParameter = derparameter, flowDirection = flowdirection, yMultiplier = ymultiplier, yUnit = yunit, DispatchSchedule = dispatchschedule, **kwargs)
        self.DERParameter = derparameter
        self.flowDirection = flowdirection
        self.yMultiplier =ymultiplier
        self.yUnit = yunit
        if dispatchschedule is None:
            self.DispatchSchedule = []
        else:
            self.DispatchSchedule = dispatchschedule


class EndDeviceGroup(ComplexModel):
    _type_info = [
        ('mRID', Unicode),
        ('DERMonitorableParameter', DERMonitorableParameter),
        ('Names', Name.customize(max_occurs="unbounded", min_occurs=0))
    ]

    def __init__(self, mrid=None, dermonitorableparameter=None, names=None, **kwargs):
        super().__init__(mRID=mrid, DERMonitorableParameter=dermonitorableparameter, Names=names, **kwargs)
        self.mRID = mrid
        self.DERMonitorableParameter = dermonitorableparameter
        if names is None:
            self.Names = []
        else:
            self.Names = names


class DERGroupDispatch(ComplexModel):
    _type_info = [
        ('mRID', Unicode),
        ('EndDeviceGroup', EndDeviceGroup),
        ('Names', Name.customize(max_occurs="unbounded", min_occurs=0))
    ]

    def __init__(self, mrid=None, enddevicegroup=None, names=None, **kwargs):
        super().__init__(mRID=mrid, EndDeviceGroup=enddevicegroup, Names=names, **kwargs)
        self.mRID = mrid
        self.EndDeviceGroup = enddevicegroup
        if names is None:
            self.Names = []
        else:
            self.Names = names


class DERGroupDispatches(ComplexModel):
    _type_info = [
        ('DERGroupDispatch', DERGroupDispatch.customize(max_occurs="unbounded", min_occurs=1)),
    ]

    def __init__(self, dergroupdispatch=None, **kwargs):
        super().__init__(DERGroupDispatch=dergroupdispatch, **kwargs)
        if dergroupdispatch is None:
            self.DERGroupDispatch = []
        else:
            self.DERGroupDispatch = dergroupdispatch
