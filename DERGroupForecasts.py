from spyne import ComplexModel, Uuid, DateTime, Float, Integer
from enums import DERUnitSymbol, DERParameterKind, FlowDirectionKind, UnitMultiplier, TimeIntervalKind, CurveStyle
import datetime as datetime_
from message import Name


class DERCurveData(ComplexModel):
    _type_info = [
        ('maxYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('minYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('nominalYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('intervalNumber', Integer.customize(max_occurs=1, min_occurs=1)),
    ]

    def __init__(self, intervalNumber=None, maxYValue=None, minYValue=None, nominalYValue=None, **kwargs):
        super().__init__(maxYValue=maxYValue, minYValue=minYValue, nominalYValue=nominalYValue, intervalNumber=intervalNumber, **kwargs)
        self.intervalNumber = intervalNumber
        self.maxYValue = maxYValue
        self.minYValue = minYValue
        self.nominalYValue = nominalYValue
# end class DERCurveData


class DispatchSchedule(ComplexModel):
    """curveStyleKind -- Used to specify whether the values over an interval are constant (constantYValue) or linearly interpolated (straightLineYValues)
    startTime -- The start time of the first interval in the dispatch schedule
    timeIntervalDuration -- The length of time for each interval in the dispatch schedule.
    timeIntervalUnit -- The unit of measure for the time axis of the dispatch schedule.

    """
    _type_info = [
        ('confidence', Float.customize(max_occurs=1, min_occurs=0)),
        ('curveStyleKind', CurveStyle.customize(max_occurs=1, min_occurs=1)),
        ('startTime', DateTime.customize(max_occurs=1, min_occurs=1)),
        ('timeIntervalDuration', Integer.customize(max_occurs=1, min_occurs=1)),
        ('timeIntervalUnit', TimeIntervalKind.customize(max_occurs=1, min_occurs=1)),
        ('DERCurveData', DERCurveData.customize(max_occurs='unbounded', min_occurs=1)),
    ]

    def __init__(self, confidence=None, curveStyleKind=None, startTime=None, timeIntervalDuration=None, timeIntervalUnit=None, DERCurveData=None, **kwargs):
        super().__init__(startTime=startTime, confidence=confidence, curveStyleKind=curveStyleKind, timeIntervalDuration=timeIntervalDuration, timeIntervalUnit=timeIntervalUnit, DERCurveData=DERCurveData, **kwargs)
        self.confidence = confidence
        self.curveStyleKind = curveStyleKind
        if isinstance(startTime, str):
            initvalue_ = datetime_.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = startTime
        self.startTime = initvalue_
        self.timeIntervalDuration = timeIntervalDuration
        self.timeIntervalUnit = timeIntervalUnit
        if DERCurveData is None:
            self.DERCurveData = []
        else:
            self.DERCurveData = DERCurveData
# end class DispatchSchedule


class DERMonitorableParameter(ComplexModel):
    _type_info = [
        ('DERParameter', DERParameterKind.customize(max_occurs=1, min_occurs=1)),
        ('flowDirection', FlowDirectionKind.customize(max_occurs=1, min_occurs=0)),
        ('yMultiplier', UnitMultiplier.customize(max_occurs=1, min_occurs=1)),
        ('yUnit', DERUnitSymbol.customize(max_occurs=1, min_occurs=1)),
        ('yUnitInstalledMax', Float.customize(max_occurs=1, min_occurs=0)),
        ('yUnitInstalledMin', Float.customize(max_occurs=1, min_occurs=0)),
        ('DispatchSchedule', DispatchSchedule.customize(max_occurs='unbounded', min_occurs=1))
    ]

    def __init__(self, dERParameter=None, flowDirection=None, yMultiplier=None, yUnit=None, yUnitInstalledMax=None, yUnitInstalledMin=None, dispatchSchedule=None, **kwargs):
        super().__init__(DERParameter=dERParameter, flowDirection=flowDirection, yMultiplier=yMultiplier, yUnit=yUnit, yUnitInstalledMax=yUnitInstalledMax, yUnitInstalledMin=yUnitInstalledMin, DispatchSchedule=dispatchSchedule, **kwargs)
        self.DERParameter = dERParameter
        self.flowDirection = flowDirection
        self.yMultiplier = yMultiplier
        self.yUnit = yUnit
        self.yUnitInstalledMax = yUnitInstalledMax
        self.yUnitInstalledMin = yUnitInstalledMin
        if dispatchSchedule is None:
            self.DispatchSchedule = []
        else:
            self.DispatchSchedule = dispatchSchedule
# end class DERMonitorableParameter


class EndDeviceGroup(ComplexModel):
    """EndDeviceGroup -- Abstraction for management of group communications within a two-way AMR system or the data for a group of related end devices. Commands can be issued to all of the end devices that belong to the group using a defined group address and the underlying AMR communication infrastructure. A DERGroup and a PANDeviceGroup is an EndDeviceGroup.
    mRID -- Master resource identifier issued by a model authority. The mRID is unique within an exchange context. Global uniqueness is easily achieved by using a UUID,  as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended.
    For CIMXML data files in RDF syntax conforming to IEC 61970-552 Edition 1, the mRID is mapped to rdf:ID or rdf:about attributes that identify CIM object elements.
    Names -- All names of this identified object.

    """
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=0)),
        ('DERMonitorableParameter', DERMonitorableParameter.customize(max_occurs='unbounded', min_occurs=1)),
        ('Names', Name.customize(max_occurs='unbounded', min_occurs=0)),
    ]

    def __init__(self, mRID=None, DERMonitorableParameter=None, Names=None, **kwargs):
        super().__init__(mRID=mRID, DERMonitorableParameter=DERMonitorableParameter, Names=Names, **kwargs)
        self.mRID = mRID
        if DERMonitorableParameter is None:
            self.DERMonitorableParameter = []
        else:
            self.DERMonitorableParameter = DERMonitorableParameter
        if Names is None:
            self.Names = []
        else:
            self.Names = Names
# end class EndDeviceGroup


class DERGroupForecast(ComplexModel):
    """mRID -- Master resource identifier issued by a model authority. The mRID is unique within an exchange context. Global uniqueness is easily achieved by using a UUID,  as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended.
    For CIMXML data files in RDF syntax conforming to IEC 61970-552 Edition 1, the mRID is mapped to rdf:ID or rdf:about attributes that identify CIM object elements.
    Names -- All names of this identified object.

    """
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=0)),
        ('predictionCreationDate',  DateTime.customize(max_occurs=1, min_occurs=1)),
        ('Names', Name.customize(max_occurs='unbounded', min_occurs=0)),
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs=1, min_occurs=1))
    ]

    def __init__(self, mRID=None, predictionCreationDate=None, endDeviceGroup=None, names=None, **kwargs):
        super().__init__(mRID=mRID, predictionCreationDate=predictionCreationDate, Names=names, EndDeviceGroup=endDeviceGroup, **kwargs)
        self.mRID = mRID
        if isinstance(predictionCreationDate, str):
            initvalue_ = datetime_.datetime.strptime(predictionCreationDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = predictionCreationDate
        self.predictionCreationDate = initvalue_
        self.EndDeviceGroup = endDeviceGroup
        if names is None:
            self.Names = []
        else:
            self.Names = names
# end class DERGroupForecast


class DERGroupForecasts(ComplexModel):
    _type_info = [
        ('DERGroupForecast', DERGroupForecast.customize(max_occurs='unbounded', min_occurs=1))
    ]

    def __init__(self, dERGroupForecast=None, **kwargs):
        super().__init__(EndDeviceGroup=dERGroupForecast, **kwargs)
        if dERGroupForecast is None:
            self.DERGroupForecast = []
        else:
            self.DERGroupForecast = dERGroupForecast
# end class DERGroupForecasts


class DateTimeInterval(ComplexModel):
    """DateTimeInterval -- Interval between two date and time points.
    end -- End date and time of this interval.
    start -- Start date and time of this interval.
    
    """
    _type_info = [
        ('start', DateTime.customize(max_occurs=1, min_occurs=1)),
        ('end', DateTime.customize(max_occurs=1, min_occurs=1)),
    ]

    def __init__(self, end=None, start=None, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
        if isinstance(end, str):
            initvalue_ = datetime_.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = end
        self.end = initvalue_
        if isinstance(start, str):
            initvalue_ = datetime_.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = start
        self.start = initvalue_
# end class DateTimeInterval