from spyne import ComplexModel, Uuid, Unicode, DateTime, Float, Enum
import datetime as datetime_


# class DERParameterKind(Enum):
#     ACTIVE_POWER='activePower'
#     APPARENT_POWER='apparentPower'
#     DECREASING_RAMP_RATE='decreasingRampRate'
#     HIGH_FILTER_BI_DIRECTIONAL_REGULATION='highFilterBiDirectionalRegulation'
#     HIGH_FILTER_DOWN_REGULATION='highFilterDownRegulation'
#     HIGH_FILTER_UP_REGULATION='highFilterUpRegulation'
#     INCREASING_RAMP_RATE='increasingRampRate'
#     LOW_FILTER_BI_DIRECTIONAL_REGULATION='lowFilterBiDirectionalRegulation'
#     LOW_FILTER_DOWN_REGULATION='lowFilterDownRegulation'
#     LOW_FILTER_UP_REGULATION='lowFilterUpRegulation'
#     REACTIVE_POWER='reactivePower'
#     VOLTAGE='voltage'


# class DERUnitSymbol(Enum):
#     """The units defined for usage in the CIM."""
#     A='A' # Current in Ampere.
#     AH='Ah' # Ampere-hours, Ampere-hours.
#     AS='As' # Ampere seconds (A·s).
#     BTU='Btu' # Energy, British Thermal Unit.
#     HZ='Hz' # Frequency in Hertz (1/s).
#     Q='Q' # Quantity power, Q.
#     QH='Qh' # Quantity energy, Qh.
#     V='V' # Electric potential in Volt (W/A).
#     VA='VA' # Apparent power in Volt Ampere (See also real power and reactive power.)
#     V_AH='VAh' # Apparent energy in Volt Ampere hours.
#     V_AR='VAr' # Reactive power in Volt Ampere reactive. The “reactive” or “imaginary” component of electrical power (VIsin(phi)). (See also real power and apparent power).Note: Different meter designs use different methods to arrive at their results. Some meters may compute reactive power as an arithmetic value, while others compute the value vectorially. The data consumer should determine the method in use and the suitability of the measurement for the intended purpose.
#     V_ARH='VArh' # Reactive energy in Volt Ampere reactive hours.
#     V_PER_VA='VPerVA' # Power factor, PF, the ratio of the active power to the apparent power. Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.
#     V_PER_V_AR='VPerVAr' # Power factor, PF, the ratio of the active power to the apparent power. Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.
#     VH='Vh' # Volt-hour, Volt hours.
#     VS='Vs' # Volt second (Ws/A).
#     W='W' # Real power in Watt (J/s). Electrical power may have real and reactive components. The real portion of electrical power (I²R or VIcos(phi)), is expressed in Watts. (See also apparent power and reactive power.)
#     W_PER_A='WPerA' # Active power per current flow, watt per Ampere.
#     W_PERS='WPers' # Ramp rate in Watt per second.
#     WH='Wh' # Real energy in Watt hours.
#     DEG='deg' # Plane angle in degrees.
#     DEG_C='degC' # Relative temperature in degrees Celsius.In the SI unit system the symbol is ºC. Electric charge is measured in coulomb that has the unit symbol C. To distinguish degree Celsius form coulomb the symbol used in the UML is degC. Reason for not using ºC is the special character º is difficult to manage in software.
#     H='h' # Time, hour = 60 min = 3600 s.
#     MIN='min' # Time, minute = 60 s.
#     OHM='ohm' # Electric resistance in ohm (V/A).
#     OHM_PERM='ohmPerm' # Electric resistance per length in ohm per metre ((V/A)/m).
#     OHMM='ohmm' # resistivity, Ohm metre, (rho).
#     ONE_PER_HZ='onePerHz' # Reciprocal of frequency (1/Hz).
#     S='s' # Time in seconds.
#     THERM='therm' # Energy, Therm.

#
# class FlowDirectionKind(Enum):
#     """Kind of flow direction for reading/measured values proper to some
#     commodities such as, for example, energy, power, demand."""
#     FORWARD='forward' # "Delivered," or "Imported" as defined 61968-2.Forward Active Energy is a positive kWh value as one would naturally expect to find as energy is supplied by the utility and consumed at the service.Forward Reactive Energy is a positive VArh value as one would naturally expect to find in the presence of inductive loading.In polyphase metering, the forward energy register is incremented when the sum of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="209" height="16" border="0" alt="graphic"/&gt;
#     LAGGING='lagging' # Typically used to describe that a power factor is lagging the reference value.Note 1: When used to describe VA, “lagging” describes a form of measurement where reactive power is considered in all four quadrants, but real power is considered only in quadrants I and IV.Note 2: When used to describe power factor, the term “Lagging” implies that the PF is negative. The term “lagging” in this case takes the place of the negative sign. If a signed PF value is to be passed by the data producer, then the direction of flow enumeration zero (none) should be used in order to avoid the possibility of creating an expression that employs a double negative. The data consumer should be able to tell from the sign of the data if the PF is leading or lagging. This principle is analogous to the concept that “Reverse” energy is an implied negative value, and to publish a negative reverse value would be ambiguous.Note 3: Lagging power factors typically indicate inductive loading.
#     LEADING='leading' # Typically used to describe that a power factor is leading the reference value.Note: Leading power factors typically indicate capacitive loading.
#     NET='net' # |Forward| - |Reverse|, See 61968-2.Note: In some systems, the value passed as a “net” value could become negative. In other systems the value passed as a “net” value is always a positive number, and rolls-over and rolls-under as needed.
#     NONE='none' # Not Applicable (N/A)
#     Q_1_MINUS_Q_4='q1minusQ4' # Q1 minus Q4
#     Q_1_PLUS_Q_2='q1plusQ2' # Reactive positive quadrants. (The term “lagging” is preferred.)
#     Q_1_PLUS_Q_3='q1plusQ3' # Quadrants 1 and 3
#     Q_1_PLUS_Q_4='q1plusQ4' # Quadrants 1 and 4 usually represent forward active energy
#     Q_2_MINUS_Q_3='q2minusQ3' # Q2 minus Q3
#     Q_2_PLUS_Q_3='q2plusQ3' # Quadrants 2 and 3 usually represent reverse active energy
#     Q_2_PLUS_Q_4='q2plusQ4' # Quadrants 2 and 4
#     Q_3_MINUS_Q_2='q3minusQ2' # Q3 minus Q2
#     Q_3_PLUS_Q_4='q3plusQ4' # Reactive negative quadrants. (The term “leading” is preferred.)
#     QUADRANT_1='quadrant1' # Q1 only
#     QUADRANT_2='quadrant2' # Q2 only
#     QUADRANT_3='quadrant3' # Q3 only
#     QUADRANT_4='quadrant4' # Q4 only
#     REVERSE='reverse' # Reverse Active Energy is equivalent to "Received," or "Exported" as defined in 61968-2.Reverse Active Energy is a positive kWh value as one would expect to find when energy is backfed by the service onto the utility network.Reverse Reactive Energy is a positive VArh value as one would expect to find in the presence of capacitive loading and a leading Power Factor.In polyphase metering, the reverse energy register is incremented when the sum of the phase energies is less than zero:&lt;img src="HTS_1.PNG" width="209" height="16" border="0" alt="graphic"/&gt;Note: The value passed as a reverse value is always a positive value. It is understood by the label “reverse” that it represents negative flow.
#     TOTAL='total' # |Forward| + |Reverse|, See 61968-2.The sum of the commodity in all quadrants Q1+Q2+Q3+Q4.In polyphase metering, the total energy register is incremented when the absolute value of the sum of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="217" height="16" border="0" alt="graphic"/&gt;
#     TOTAL_BY_PHASE='totalByPhase' # In polyphase metering, the total by phase energy register is incremented when the sum of the absolute values of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="234" height="16" border="0" alt="graphic"/&gt;In single phase metering, the formulas for “Total” and “Total by phase” collapse to the same expression. For communication purposes however, the “Total” enumeration should be used with single phase meter data.

#
# class UnitMultiplier(Enum):
#     """The unit multipliers defined for the CIM. When applied to unit symbols
#     that already contain a multiplier, both multipliers are used. For
#     example, to exchange kilograms using unit symbol of kg, one uses the
#     "none" multiplier, to exchange metric ton (Mg), one uses the "k"
#     multiplier."""
#     E='E' # Exa 10**18.
#     G='G' # Giga 10**9.
#     M='M' # Mega 10**6.
#     P='P' # Peta 10**15
#     T='T' # Tera 10**12.
#     Y='Y' # Yotta 10**24
#     Z='Z' # Zetta 10**21
#     A='a' # atto 10**-18.
#     C='c' # Centi 10**-2.
#     D='d' # Deci 10**-1.
#     DA='da' # deca 10**1.
#     F='f' # femto 10**-15.
#     H='h' # hecto 10**2.
#     K='k' # Kilo 10**3.
#     M_1='m' # Milli 10**-3.
#     MICRO='micro' # Micro 10**-6.
#     N='n' # Nano 10**-9.
#     NONE='none' # No multiplier or equivalently multiply by 1.
#     P_1='p' # Pico 10**-12.
#     Y_1='y' # yocto 10**-24.
#     Z_1='z' # zepto 10**-21.


DERParameterKind = Enum(
    'activePower',
    'apparentPower',
    'decreasingRampRate',
    'highFilterBiDirectionalRegulation',
    'highFilterDownRegulation',
    'highFilterUpRegulation',
    'increasingRampRate',
    'lowFilterBiDirectionalRegulation',
    'lowFilterDownRegulation',
    'lowFilterUpRegulation',
    'reactivePower',
    'voltage', type_name='DERParameterKind')


"""The units defined for usage in the CIM."""
DERUnitSymbol = Enum(
    'A', # Current in Ampere.
    'Ah', # Ampere-hours, Ampere-hours.
    'As', # Ampere seconds (A·s).
    'Btu', # Energy, British Thermal Unit.
    'Hz', # Frequency in Hertz (1/s).
    'Q', # Quantity power, Q.
    'Qh', # Quantity energy, Qh.
    'V', # Electric potential in Volt (W/A).
    'VA', # Apparent power in Volt Ampere (See also real power and reactive power.)
    'VAh', # Apparent energy in Volt Ampere hours.
    'VAr', # Reactive power in Volt Ampere reactive. The “reactive” or “imaginary” component of electrical power (VIsin(phi)). (See also real power and apparent power).Note: Different meter designs use different methods to arrive at their results. Some meters may compute reactive power as an arithmetic value, while others compute the value vectorially. The data consumer should determine the method in use and the suitability of the measurement for the intended purpose.
    'VArh', # Reactive energy in Volt Ampere reactive hours.
    'VPerVA', # Power factor, PF, the ratio of the active power to the apparent power. Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.
    'VPerVAr', # Power factor, PF, the ratio of the active power to the apparent power. Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.
    'Vh', # Volt-hour, Volt hours.
    'Vs', # Volt second (Ws/A).
    'W', # Real power in Watt (J/s). Electrical power may have real and reactive components. The real portion of electrical power (I²R or VIcos(phi)), is expressed in Watts. (See also apparent power and reactive power.)
    'WPerA', # Active power per current flow, watt per Ampere.
    'WPers', # Ramp rate in Watt per second.
    'Wh', # Real energy in Watt hours.
    'deg', # Plane angle in degrees.
    'degC', # Relative temperature in degrees Celsius.In the SI unit system the symbol is ºC. Electric charge is measured in coulomb that has the unit symbol C. To distinguish degree Celsius form coulomb the symbol used in the UML is degC. Reason for not using ºC is the special character º is difficult to manage in software.
    'h', # Time, hour = 60 min = 3600 s.
    'min', # Time, minute = 60 s.
    'ohm', # Electric resistance in ohm (V/A).
    'ohmPerm', # Electric resistance per length in ohm per metre ((V/A)/m).
    'ohmm', # resistivity, Ohm metre, (rho).
    'onePerHz', # Reciprocal of frequency (1/Hz).
    's', # Time in seconds.
    'therm', # Energy, Therm.
    type_name='DERUnitSymbol')


"""Kind of flow direction for reading/measured values proper to some
commodities such as, for example, energy, power, demand."""
FlowDirectionKind = Enum(
    'forward', # "Delivered," or "Imported" as defined 61968-2.Forward Active Energy is a positive kWh value as one would naturally expect to find as energy is supplied by the utility and consumed at the service.Forward Reactive Energy is a positive VArh value as one would naturally expect to find in the presence of inductive loading.In polyphase metering, the forward energy register is incremented when the sum of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="209" height="16" border="0" alt="graphic"/&gt;
    'lagging', # Typically used to describe that a power factor is lagging the reference value.Note 1: When used to describe VA, “lagging” describes a form of measurement where reactive power is considered in all four quadrants, but real power is considered only in quadrants I and IV.Note 2: When used to describe power factor, the term “Lagging” implies that the PF is negative. The term “lagging” in this case takes the place of the negative sign. If a signed PF value is to be passed by the data producer, then the direction of flow enumeration zero (none) should be used in order to avoid the possibility of creating an expression that employs a double negative. The data consumer should be able to tell from the sign of the data if the PF is leading or lagging. This principle is analogous to the concept that “Reverse” energy is an implied negative value, and to publish a negative reverse value would be ambiguous.Note 3: Lagging power factors typically indicate inductive loading.
    'leading', # Typically used to describe that a power factor is leading the reference value.Note: Leading power factors typically indicate capacitive loading.
    'net', # |Forward| - |Reverse|, See 61968-2.Note: In some systems, the value passed as a “net” value could become negative. In other systems the value passed as a “net” value is always a positive number, and rolls-over and rolls-under as needed.
    'none', # Not Applicable (N/A)
    'q1minusQ4', # Q1 minus Q4
    'q1plusQ2', # Reactive positive quadrants. (The term “lagging” is preferred.)
    'q1plusQ3', # Quadrants 1 and 3
    'q1plusQ4', # Quadrants 1 and 4 usually represent forward active energy
    'q2minusQ3', # Q2 minus Q3
    'q2plusQ3', # Quadrants 2 and 3 usually represent reverse active energy
    'q2plusQ4', # Quadrants 2 and 4
    'q3minusQ2', # Q3 minus Q2
    'q3plusQ4', # Reactive negative quadrants. (The term “leading” is preferred.)
    'quadrant1', # Q1 only
    'quadrant2', # Q2 only
    'quadrant3', # Q3 only
    'quadrant4', # Q4 only
    'reverse', # Reverse Active Energy is equivalent to "Received," or "Exported" as defined in 61968-2.Reverse Active Energy is a positive kWh value as one would expect to find when energy is backfed by the service onto the utility network.Reverse Reactive Energy is a positive VArh value as one would expect to find in the presence of capacitive loading and a leading Power Factor.In polyphase metering, the reverse energy register is incremented when the sum of the phase energies is less than zero:&lt;img src="HTS_1.PNG" width="209" height="16" border="0" alt="graphic"/&gt;Note: The value passed as a reverse value is always a positive value. It is understood by the label “reverse” that it represents negative flow.
    'total', # |Forward| + |Reverse|, See 61968-2.The sum of the commodity in all quadrants Q1+Q2+Q3+Q4.In polyphase metering, the total energy register is incremented when the absolute value of the sum of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="217" height="16" border="0" alt="graphic"/&gt;
    'totalByPhase', # In polyphase metering, the total by phase energy register is incremented when the sum of the absolute values of the phase energies is greater than zero:&lt;img src="HTS_1.PNG" width="234" height="16" border="0" alt="graphic"/&gt;In single phase metering, the formulas for “Total” and “Total by phase” collapse to the same expression. For communication purposes however, the “Total” enumeration should be used with single phase meter data.
     type_name='FlowDirectionKind')


"""The unit multipliers defined for the CIM. When applied to unit symbols
that already contain a multiplier, both multipliers are used. For
example, to exchange kilograms using unit symbol of kg, one uses the
"none" multiplier, to exchange metric ton (Mg), one uses the "k"
multiplier."""
UnitMultiplier = Enum(
    'E', # Exa 10**18.
    'G', # Giga 10**9".
    'M', # Mega 10**6.
    'P', # Peta 10**15
    'T', # Tera 10**12.
    'Y', # Yotta 10**24
    'Z', # Zetta 10**21
    'a', # atto 10**-18.
    'c', # Centi 10**-2.
    'd', # Deci 10**-1.
    'da', # deca 10**1.
    'f', # femto 10**-15.
    'h', # hecto 10**2.
    'k', # Kilo 10**3.
    'm', # Milli 10**-3.
    'micro', # Micro 10**-6.
    'n', # Nano 10**-9.
    'none', # No multiplier or equivalently multiply by 1.
    'p', # Pico 10**-12.
    'y', # yocto 10**-24.
    'z', # zepto 10**-21.
    type_name='UnitMultiplier')


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
        ('DERParameter', DERParameterKind.customize(max_occurs=1, min_occurs=1)),
        ('flowDirection', FlowDirectionKind.customize(max_occurs=1, min_occurs=0)),
        ('yMultiplier', UnitMultiplier.customize(max_occurs=1, min_occurs=1)),
        ('yUnit', DERUnitSymbol.customize(max_occurs=1, min_occurs=1)),
        ('yUnitInstalledMax', Float.customize(max_occurs=1, min_occurs=0)),
        ('yUnitInstalledMin', Float.customize(max_occurs=1, min_occurs=0)),
        ('DERCurveData', DERCurveData.customize(max_occurs=1, min_occurs=1))
    ]

    def __init__(self, dERParameter=None, flowDirection=None, yMultiplier=None, yUnit=None, yUnitInstalledMax=None, yUnitInstalledMin=None, DERCurveData=None, **kwargs):
        super().__init__(DERParameter=dERParameter, flowDirection=flowDirection, yMultiplier=yMultiplier, yUnit=yUnit, yUnitInstalledMax=yUnitInstalledMax, yUnitInstalledMin=yUnitInstalledMin, **kwargs)
        self.DERParameter = dERParameter
        self.flowDirection = flowDirection
        self.yMultiplier = yMultiplier
        self.yUnit = yUnit
        self.yUnitInstalledMax = yUnitInstalledMax
        self.yUnitInstalledMin = yUnitInstalledMin
        self.DERCurveData = DERCurveData
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
            self.DERMonitorableParameter = []
        else:
            self.DERMonitorableParameter = dERMonitorableParameter
        if names is None:
            self.Names = []
        else:
            self.Names = names
        self.status = status
# end class EndDeviceGroup


class DERGroupStatuses(ComplexModel):
    _type_info = [
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs='unbounded', min_occurs=1))
    ]

    def __init__(self, endDeviceGroup=None, **kwargs):
        super().__init__(EndDeviceGroup=endDeviceGroup, **kwargs)
        if endDeviceGroup is None:
            self.EndDeviceGroup = []
        else:
            self.EndDeviceGroup = endDeviceGroup
# end class DERGroupStatuses