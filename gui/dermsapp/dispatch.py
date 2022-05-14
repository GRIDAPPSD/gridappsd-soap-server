import jsons
import os
from threading import Lock

__groups = {}

write_lock = Lock()

class Dispatch:
    '''
    class represent a DER Group Dispatch
    '''
    def __init__(self, mRID, EndDeviceGroup, Names):
        self.mRID = mRID
        self.EndDeviceGroup = EndDeviceGroup
        self.Names = Names

    def tojson(self):
        return self.__dict__

    def __repr__(self):
        return jsons.dumps(self.__dict__)

class Dispatch_group:
    def __init__(self, mRID, DERMonitorableParameter, Names):
        self.mRID = mRID
        self.DERMonitorableParameter = DERMonitorableParameter
        self.Names = Names

    def tojson(self):
        return self.__dict__

    def __repr__(self):
        return jsons.dumps(self.__dict__)

class Dispatch_parameter:
    def __init__(self, DERParameter, flowDirection, yMultiplier, yUnit, DispatchSchedule):
        self.DERParameter = DERParameter
        self.flowDirection = flowDirection
        self.yMultiplier = yMultiplier
        self.yUnit = yUnit
        self.DispatchSchedule = DispatchSchedule

    def tojson(self):
        return self.__dict__

    def __repr__(self):
        return jsons.dumps(self.__dict__)

class Dispatch_schedule:
    def __init__(self, curveStyleKind, startTime, timeIntervalDuration, timeIntervalUnit, DERCurveData):
        self.curveStyleKind = curveStyleKind
        self.startTime = startTime
        self.timeIntervalDuration = timeIntervalDuration
        self.timeIntervalUnit = timeIntervalUnit
        self.DERCurveData = DERCurveData

    def tojson(self):
        return self.__dict__

    def __repr__(self):
        return jsons.dumps(self.__dict__)


class Dispatch_curvedata:
    '''
    class represent a DER Group Dispatch
    '''
    def __init__(self, intervalNumber, nominalYValue):

        self.intervalNumber = intervalNumber
        self.nominalYValue = nominalYValue

    def tojson(self):
        return self.__dict__

    def __repr__(self):
        return jsons.dumps(self.__dict__)
