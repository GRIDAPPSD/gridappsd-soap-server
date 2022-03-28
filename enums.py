from spyne import Enum

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
    'voltage',
    'stateOfCharge', type_name='DERParameterKind')


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


TimeIntervalKind = Enum(
    'D',
    'M',
    'Y',
    'h',
    'm',
    's', type_name='TimeIntervalKind')

"""Style or shape of curve."""
CurveStyle = Enum(
    'constantYValue',   # The Y-axis values are assumed constant until the next curve point and prior to the first curve point.
    'straightLineYValues',  # The Y-axis values are assumed to be a straight line between values.  Also known as linear interpolation.
    type_name='CurveStyle')