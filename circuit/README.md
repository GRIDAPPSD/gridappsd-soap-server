# Creating Test Circuit for DERMS Interop

Copyright (c) 2017-2021, Battelle Memorial Institute

## Contents

The archived files include:

1. The base CIM XML and UUID files are in _Transactive.xml_ and _transactive_uuids.dat_. 
2. The CIM house UUID values are maintained in _Transactive_house_uuids.json_.
3. The CIM DER specifications and UUID values are in _Transactive_der.dat_ and _Transactive_der_uuid.dat_.
4. The CIM measurement UUID values are maintained in _Transactive_msid.json_
5. The original OpenDSS model files are in _*.dss_, with map coordinates in _Buscoords.csv_

## Uploading Process

The test case upload is performed with ```python3 upload_circuit.py```. This relies on completing the test case conversion and validation as described below, with results archived in the repository. The upload script does these steps:

1. Empty the database
2. Upload the CIM XML to Blazegraph
3. Insert Houses. There are 1697 of these at 1280 EnergyConsumer locations.
4. Insert DER. Near the substation, there is a 2-MW Synchronous Machine (Wind) with 2-MW, 4-hour battery. Out on the feeder, there is a 2-MW PV installation with a 2-MW, 4-hour battery. There are also 1134 rooftop PV, rated 3 kW each, installed at 90% of the EnergyConsumer locations.
5. List and insert CIM measurement points on the feeder

A developer following this process should have the Blazegraph container installed, and the CIMHub repository cloned from GitHub. From the local CIMHub directory, invoke ```pip3 install -e .``` because the cimhub package on PyPi may not have the latest features and fixes. However, it is not necessary to build the CIMImporter Java program, nor use OpenDSS or GridLAB-D, in following this process.

## Conversion and Validation Process

The test case conversion is executed with ```python3 make_circuit.py```. The steps cover:

1. Solve the original GridAPPS-D case in OpenDSS, then create CIM XML
2. Upload the CIM XML to Blazegraph
3. Insert Houses. There are 1697 of these at 1280 EnergyConsumer locations.
4. Insert DER. Near the substation, there is a 2-MW Synchronous Machine (Wind) with 2-MW, 4-hour battery. Out on the feeder, there is a 2-MW PV installation with a 2-MW, 4-hour battery. There are also 1134 rooftop PV, rated 3 kW each, installed at 90% of the EnergyConsumer locations.
5. List and insert CIM measurement points on the feeder
6. Export CSV, DSS, and GridLAB-D (GLM) files from Blazegraph
7. Solve the exported models in OpenDSS and GridLAB-D
8. Compare the original OpenDSS power flow result with exported OpenDSS and GridLAB-D power flow results

The test cases are configured by entries in the ```cases``` array near the top of ```test_OEDI.py```.
Each array element is a dictionary with the following keys:

- **root** is used to generate file names for converted files
- **mRID** is a UUID4 to make the test case feeder unique. For a new test case, generate a random new mRID with this Python script: ```import uuid;idNew=uuid.uuid4();print(str(idNew).upper())```'
- **glmvsrc** is the substation source line-to-neutral voltage for GridLAB-D
- **bases** is an array of voltage bases to use for interpretation of the voltage outputs. Specify line-to-line voltages, in ascending order, leaving out 208 and 480.
- **export_options** is a string of command-line options to the CIMImporter Java program. ```-e=carson``` keeps the OpenDSS line constants model compatible with GridLAB-D's
- **skip_gld** specify as ```True``` when you know that GridLAB-D won't support this test case
- **check_branches** an array of branches in the model to compare power flows and line-to-line voltages. Each element contains:
    - **dss_link** is the name of an OpenDSS branch for power and current flow; power delivery or power conversion components may be used
    - **dss_bus** is the name of an OpenDSS bus attached to **dss_link**. Line-to-line voltages are calculated here, and this bus establishes flow polarity into the branch at this bus.
    - **gld_link** is the name of a GridLAB-D branch for power and current flow; only links, e.g., line or transformer, may be used. Do not use this when **skip_gld** is ```True```
    - **gld_bus** is the name of a GridLAB-D bus attached to **gld_link**. Do not use this when **skip_gld** is ```True```

The script outputs include the comparisons requested from **check_branches**, and summary information:

- **Nbus** is the number of buses found in [Base OpenDSS, Converted OpenDSS, Converted GridLAB-D]
- **Nlink** is the number of links found in [Base OpenDSS, Converted OpenDSS, Converted GridLAB-D]
- **MAEv** is the mean absolute voltage error between Base OpenDSS and [Converted OpenDSS, Converted GridLAB-D], in per-unit. This is based on line-to-neutral voltages.
In an ungrounded system, MAEv can be large. Use the line-to-line voltage comparisons from **check_branches** for ungrounded systems.
- **MAEi** is the mean absolute link current error between Base OpenDSS and [Converted OpenDSS, Converted GridLAB-D], in Amperes

## Results

The first comparison excludes DER and house loads, i.e., the power flow results should all match.

The second comparison includes DER, which reduces feeder loading in the exported models compared to the original OpenDSS case. In GridLAB-D,
some of the load is represented with houses from the residential module, which increases feeder loading compared to both original
and exported OpenDSS cases.

```
WITHOUT HOUSES or DER

  OpenDSS branch flow in LINE.LINE_L114 from NODE_135, Base case
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2336.79 -0.0663    157.56 -0.0939    368.056 + j    10.152     AB     4065.41  0.4871
    B   2413.32 -2.1206    130.77 -2.1485    315.464 + j     8.812     BC     4132.83 -1.6093
    C   2346.76  2.0595    106.04  2.0345    248.782 + j     6.210     CA     4092.36  2.5662
    Total S =   932.303 + j    25.174
  OpenDSS branch flow in LINE.LINE_L114 from NODE_135, Converted case
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2338.38 -0.0646    157.46 -0.0932    368.046 + j    10.538     AB     4069.61  0.4878
    B   2414.14 -2.1206    130.72 -2.1480    315.470 + j     8.647     BC     4132.46 -1.6084
    C   2347.90  2.0612    105.99  2.0351    248.771 + j     6.514     CA     4094.74  2.5680
    Total S =   932.287 + j    25.698
  GridLAB-D branch flow in LINE_LINE_L114 from NODE_135
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2339.35 -0.0609    146.78 -0.0882    343.233 + j     9.356     AB     4071.05  0.4880
    B   2407.73  4.1613    129.85  4.1343    312.541 + j     8.432     BC     4128.89 -1.6078
    C   2352.17  2.0613    100.13  2.0361    235.446 + j     5.934     CA     4095.23  2.5695
    Total S =   891.219 + j    23.722
Transactive      Nbus=[  3036,  3036,  5602] Nlink=[  5507,  5507,   690] MAEv=[ 0.0006, 0.0028] MAEi=[   0.0099,   1.9438]

WITH DER and WITH HOUSES (GridLAB-D only)
  OpenDSS branch flow in LINE.LINE_L114 from NODE_135, Base case
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2336.79 -0.0663    157.56 -0.0939    368.056 + j    10.152     AB     4065.41  0.4871
    B   2413.32 -2.1206    130.77 -2.1485    315.464 + j     8.812     BC     4132.83 -1.6093
    C   2346.76  2.0595    106.04  2.0345    248.782 + j     6.210     CA     4092.36  2.5662
    Total S =   932.303 + j    25.174
  OpenDSS branch flow in LINE.LINE_L114 from NODE_135, Converted case
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2440.46  0.0087     24.25 -0.0719     58.992 + j     4.767     AB     4215.11  0.5354
    B   2436.59 -2.0787     17.82 -2.1522     43.298 + j     3.187     BC     4213.28 -1.5549
    C   2430.94  2.1118     12.83  2.0282     31.079 + j     2.604     CA     4229.35  2.6322
    Total S =   133.369 + j    10.559
  GridLAB-D branch flow in LINE_LINE_L114 from NODE_135
  Phs     Volts     rad      Amps     rad         kW          kVAR   PhsPhs     Volts     rad
    A   2365.35 -0.0079     90.80 -0.5735    181.334 + j   115.096     AB     4122.36  0.5292
    B   2415.24  4.1957     72.74  3.5972    145.152 + j    98.979     BC     4142.99 -1.5677
    C   2372.53  2.1041     70.28  1.5830    144.609 + j    83.008     CA     4123.87  2.6180
    Total S =   471.094 + j   297.083
Transactive      Nbus=[  3036,  3036,  7882] Nlink=[  5507,  7787,   690] MAEv=[ 0.0467, 0.0140] MAEi=[   8.0245,  42.8178]
```

