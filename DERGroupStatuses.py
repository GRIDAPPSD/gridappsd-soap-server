from spyne import ComplexModel, Uuid, Unicode, DateTime, Float
import datetime as datetime_


class DERCurveData(ComplexModel):
    _type_info = [
        ('maxYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('minYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('nominalYValue', Float.customize(max_occurs=1, min_occurs=0)),
        ('timeStamp',  DateTime.customize(max_occurs=1, min_occurs=1)),
    ]

    def __init__(self, maxYValue=None, minYValue=None, nominalYValue=None, timeStamp=None, **kwargs):
        super().__init__(maxYValue=maxYValue, minYValue=minYValue, nominalYValue=nominalYValue, timeStamp=timeStamp, **kwargs)
        self.maxYValue = maxYValue
        self.minYValue = minYValue
        self.nominalYValue = nominalYValue
        if isinstance(timeStamp, str):
            initvalue_ = datetime_.datetime.strptime(timeStamp, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = timeStamp
        self.timeStamp = initvalue_
# end class DERCurveData


class DERMonitorableParameter(ComplexModel):
    _type_info = [
        ('DERParameter', ['DERParameterKind', 'xs:string'], 0, 0, {'maxOccurs': '1', 'minOccurs': '1', 'name': 'DERParameter', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.DERParameter', 'type': 'xs:string'}, None),
        ('flowDirection', ['FlowDirectionKind', 'xs:string'], 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'flowDirection', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.flowDirection', 'type': 'xs:string'}, None),
        ('yMultiplier', ['UnitMultiplier', 'xs:string'], 0, 0, {'maxOccurs': '1', 'minOccurs': '1', 'name': 'yMultiplier', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.yMultiplier', 'type': 'xs:string'}, None),
        ('yUnit', ['DERUnitSymbol', 'xs:string'], 0, 0, {'maxOccurs': '1', 'minOccurs': '1', 'name': 'yUnit', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.yUnit', 'type': 'xs:string'}, None),
        ('yUnitInstalledMax', 'xs:float', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'yUnitInstalledMax', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.yUnitInstalledMax', 'type': 'xs:float'}, None),
        ('yUnitInstalledMin', 'xs:float', 0, 1, {'maxOccurs': '1', 'minOccurs': '0', 'name': 'yUnitInstalledMin', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.yUnitInstalledMin', 'type': 'xs:float'}, None),
        ('DERCurveData', 'DERCurveData', 0, 0, {'maxOccurs': '1', 'minOccurs': '1', 'name': 'DERCurveData', 'sawsdl:modelReference': 'http://iec.ch/TC57/CIM-generic#DERMonitorableParameter.DERCurveData', 'type': 'DERCurveData'}, None),
    ]

    def __init__(self, DERParameter=None, flowDirection=None, yMultiplier=None, yUnit=None, yUnitInstalledMax=None, yUnitInstalledMin=None, DERCurveData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DERParameter = DERParameter
        self.validate_DERParameterKind(self.DERParameter)
        self.DERParameter_nsprefix_ = None
        self.flowDirection = flowDirection
        self.validate_FlowDirectionKind(self.flowDirection)
        self.flowDirection_nsprefix_ = None
        self.yMultiplier = yMultiplier
        self.validate_UnitMultiplier(self.yMultiplier)
        self.yMultiplier_nsprefix_ = None
        self.yUnit = yUnit
        self.validate_DERUnitSymbol(self.yUnit)
        self.yUnit_nsprefix_ = None
        self.yUnitInstalledMax = yUnitInstalledMax
        self.yUnitInstalledMax_nsprefix_ = None
        self.yUnitInstalledMin = yUnitInstalledMin
        self.yUnitInstalledMin_nsprefix_ = None
        self.DERCurveData = DERCurveData
        self.DERCurveData_nsprefix_ = None
# end class DERMonitorableParameter


class NameTypeAuthority(ComplexModel):
    """Authority responsible for creation and management of names of a given
    type; typically an organization or an enterprise system."""
    _type_info = [
        ('description', Unicode.customize(max_occurs=1, min_occurs=0)),
        ('name', Unicode.customize(max_occurs=1, min_occurs=1)),
    ]

    def __init__(self, description=None, name=None, **kwargs):
        super().__init__(description=description, name=name, **kwargs)
        self.description = description
        self.name = name
# end class NameTypeAuthority


class NameType(ComplexModel):
    """Type of name. Possible values for attribute 'name' are implementation
    dependent but standard profiles may specify types. An enterprise may
    have multiple IT systems each having its own local name for the same
    object, e.g. a planning system may have different names from an EMS. An
    object may also have different names within the same IT system, e.g.
    localName as defined in CIM version 14. The definition from CIM14
    is:The localName is a human readable name of the object. It is a free
    text name local to a node in a naming hierarchy similar to a file
    directory structure. A power system related naming hierarchy may be:
    Substation, VoltageLevel, Equipment etc. Children of the same parent in
    such a hierarchy have names that typically are unique among them."""
    member_data_items_ = [
        ('description', Unicode.customize(max_occurs=1, min_occurs=0)),
        ('name', Unicode.customize(max_occurs=1, min_occurs=1)),
        ('NameTypeAuthority', NameTypeAuthority.customize(max_occurs=1, min_occurs=0))
    ]

    def __init__(self, description=None, name=None, nameTypeAuthority=None, **kwargs):
        super().__init__(description=description, name=name, NameTypeAuthority=nameTypeAuthority, **kwargs)
        self.description = description
        self.name = name
        self.nameTypeAuthority = nameTypeAuthority
# end class NameType


class Name(ComplexModel):
    """The Name class provides the means to define any number of human readable
    names for an object. A name is <b>not</b> to be used for defining
    inter-object relationships. For inter-object relationships instead use
    the object identification 'mRID'."""
    _type_info = [
        ('name', Unicode.customize(max_occurs=1, min_occurs=1)),
        ('NameType', NameType.customize(max_occurs=1, min_occurs=0))
    ]

    def __init__(self, name=None, nameType=None, **kwargs):
        super().__init__(name=name, NameType=nameType, **kwargs)
        self.name = name
        self.nameType = nameType
# end class Name


class Status(ComplexModel):
    """Current status information relevant to an entity."""
    _type_info = [
        ('dateTime', DateTime.customize(max_occurs=1, min_occurs=0)),
        ('reason', Unicode.customize(max_occurs=1, min_occurs=0)),
        ('remark', Unicode.customize(max_occurs=1, min_occurs=0)),
        ('value', Unicode.customize(max_occurs=1, min_occurs=0)),
    ]

    def __init__(self, dateTime=None, reason=None, remark=None, value=None, **kwargs):
        super().__init__(dateTime=dateTime, reason=reason, remark=remark, value=value, **kwargs)
        if isinstance(dateTime, str):
            initvalue_ = datetime_.datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = dateTime
        self.dateTime = initvalue_
        self.reason = reason
        self.remark = remark
        self.value = value
# end class Status


class EndDeviceGroup(ComplexModel):
    """Abstraction for management of group communications within a two-way AMR
    system or the data for a group of related end devices. Commands can be
    issued to all of the end devices that belong to the group using a
    defined group address and the underlying AMR communication
    infrastructure. A DERGroup and a PANDeviceGroup is an
    EndDeviceGroup."""
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=0)),
        ('DERMonitorableParameter', DERMonitorableParameter.customize(max_occurs='unbounded', min_occurs=1)),
        ('Names', Name.customize(max_occurs='unbounded', min_occurs=0)),
        ('status', Status.customize(max_occurs=1, min_occurs=0))
    ]

    def __init__(self, mRID=None, dERMonitorableParameter=None, names=None, status=None, **kwargs):
        super().__init__(mRID=mRID, DERMonitorableParameter=dERMonitorableParameter, Names=names, status=status, **kwargs)
        self.mRID = mRID
        if dERMonitorableParameter is None:
            self.dERMonitorableParameter = []
        else:
            self.dERMonitorableParameter = dERMonitorableParameter
        if names is None:
            self.names = []
        else:
            self.names = names
        self.status = status
# end class EndDeviceGroup


class DERGroupStatuses(ComplexModel):
    _type_info = [
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs='unbounded', min_occurs=1))
    ]

    def __init__(self, endDeviceGroup=None, **kwargs):
        super().__init__(EndDeviceGroup=endDeviceGroup)
        if endDeviceGroup is None:
            self.endDeviceGroup = []
        else:
            self.endDeviceGroup = endDeviceGroup
# end class DERGroupStatuses