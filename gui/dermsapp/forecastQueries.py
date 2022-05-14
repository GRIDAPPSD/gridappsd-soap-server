from group import Group
import datetime


# class DERMonitorableParameter():
#     def __init__(self, DERParameter=None, flowDirection=None, **kwargs):
#         super().__init__(DERParameter=DERParameter, flowDirection=flowDirection, **kwargs)
#         self.DERParameter = DERParameter
#         self.flowDirection = flowDirection


class DispatchSchedule():
    def __init__(self, curveStyleKind=None, numberOfIntervals=None, startTime=None, timeIntervalDuration=None,
                 timeIntervalUnit=None, **kwargs):
        self.curveStyleKind = curveStyleKind
        self.numberOfIntervals = numberOfIntervals
        if isinstance(startTime, str):
            initvalue_ = datetime.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = startTime
        self.startTime = initvalue_
        self.timeIntervalDuration = timeIntervalDuration
        self.timeIntervalUnit = timeIntervalUnit


class DERGroupForecastQueries():
    def __init__(self, DERMonitorableParameter=None, DispatchSchedule=None, EndDeviceGroup=None, **kwargs):
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
