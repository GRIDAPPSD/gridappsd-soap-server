import datetime as datetime_
from spyne import ComplexModel, Uuid, DateTime, Integer
from message import Name
from enums import DERParameterKind, FlowDirectionKind, TimeIntervalKind, CurveStyle


class DERMonitorableParameter(ComplexModel):
    _type_info = [
        ('DERParameter', DERParameterKind.customize(max_occurs=1, min_occurs=1)),
        ('flowDirection', FlowDirectionKind.customize(max_occurs=1, min_occurs=0)),
    ]

    def __init__(self, DERParameter=None, flowDirection=None, **kwargs):
        super().__init__(DERParameter=DERParameter, flowDirection=flowDirection, **kwargs)
        self.DERParameter = DERParameter
        self.flowDirection = flowDirection
# end class DERMonitorableParameter


class DispatchSchedule(ComplexModel):
    """curveStyleKind -- Used to specify whether the values over an interval are constant (constantYValue) or linearly interpolated (straightLineYValues)
    numberOfIntervals -- Used to specify the number of intervals when requesting a forecast or a dispatch.
    startTime -- The start time of the first interval in the dispatch schedule
    timeIntervalDuration -- The length of time for each interval in the dispatch schedule.
    timeIntervalUnit -- The unit of measure for the time axis of the dispatch schedule.

    """
    _type_info = [
        ('curveStyleKind', CurveStyle.customize(max_occurs=1, min_occurs=1)),
        ('numberOfIntervals', Integer.customize(max_occurs=1, min_occurs=1)),
        ('startTime', DateTime.customize(max_occurs=1, min_occurs=1)),
        ('timeIntervalDuration', Integer.customize(max_occurs=1, min_occurs=1)),
        ('timeIntervalUnit', TimeIntervalKind.customize(max_occurs=1, min_occurs=1)),
    ]

    def __init__(self, curveStyleKind=None, numberOfIntervals=None, startTime=None, timeIntervalDuration=None,
                 timeIntervalUnit=None, **kwargs):
        super().__init__(startTime=startTime, numberOfIntervals=numberOfIntervals, curveStyleKind=curveStyleKind,
                         timeIntervalDuration=timeIntervalDuration, timeIntervalUnit=timeIntervalUnit, **kwargs)
        self.curveStyleKind = curveStyleKind
        self.numberOfIntervals = numberOfIntervals
        if isinstance(startTime, str):
            initvalue_ = datetime_.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = startTime
        self.startTime = initvalue_
        self.timeIntervalDuration = timeIntervalDuration
        self.timeIntervalUnit = timeIntervalUnit
# end class DispatchSchedule


class EndDeviceGroup(ComplexModel):
    """EndDeviceGroup -- Abstraction for management of group communications within a two-way AMR system or the data for a group of related end devices. Commands can be issued to all of the end devices that belong to the group using a defined group address and the underlying AMR communication infrastructure. A DERGroup and a PANDeviceGroup is an EndDeviceGroup.
    mRID -- Master resource identifier issued by a model authority. The mRID is unique within an exchange context. Global uniqueness is easily achieved by using a UUID,  as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended.
    For CIMXML data files in RDF syntax conforming to IEC 61970-552 Edition 1, the mRID is mapped to rdf:ID or rdf:about attributes that identify CIM object elements.
    Names -- All names of this identified object.

    """
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=0)),
        ('Names', Name.customize(max_occurs='unbounded', min_occurs=0)),
    ]

    def __init__(self, mRID=None, Names=None, **kwargs):
        super().__init__(mRID=mRID, Names=Names, **kwargs)
        self.mRID = mRID
        if Names is None:
            self.Names = []
        else:
            self.Names = Names
# end class EndDeviceGroup


class DERGroupForecastQueries(ComplexModel):
    _type_info = [
        ('DERMonitorableParameter', DERMonitorableParameter.customize(max_occurs='unbounded', min_occurs=1)),
        ('DispatchSchedule', DispatchSchedule.customize(max_occurs='unbounded', min_occurs=1)),
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs='unbounded', min_occurs=1)),
    ]

    def __init__(self, DERMonitorableParameter=None, DispatchSchedule=None, EndDeviceGroup=None, **kwargs):
        super().__init__(DERMonitorableParameter=DERMonitorableParameter, DispatchSchedule=DispatchSchedule, EndDeviceGroup=EndDeviceGroup, **kwargs)
        if DERMonitorableParameter is None:
            self.DERMonitorableParameter = []
        else:
            self.DERMonitorableParameter = DERMonitorableParameter
        if DispatchSchedule is None:
            self.DispatchSchedule = []
        else:
            self.DispatchSchedule = DispatchSchedule
        if EndDeviceGroup is None:
            self.EndDeviceGroup = []
        else:
            self.EndDeviceGroup = EndDeviceGroup
# end class DERGroupForecastQueries
