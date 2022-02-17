# DERMS Reference Application

The Distributed Energy Resource Management System (DERMS) Reference Application
provides minimum functionality for a DERMS. It can be used for demonstrations,
or the starting point for other DERMS implementations that run in GridAPPS-D.
As depicted below, key features of this DERMS Reference Application include:

- Support for IEC 61968-5:2020, "Application integration at electric utilities - System interfaces for distribution management - Part 5: Distributed energy optimization"
- Managing DER groups
- Allocating group dispatch commands from IEC 61968-5 to individual DER units, e.g., participation weighted by DER capacity
- Updated visual displays in a running GridAPPS-D simulation
- Reporting DER group outputs via IEC 61968-5 messages

GridAPPS-D also manages the connection of DER units to the network model in CIM.

![DERMS Test Application](doc/derms_app.png)