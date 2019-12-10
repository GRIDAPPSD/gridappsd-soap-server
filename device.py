import json
from spyne import ComplexModel, Unicode, Iterable, Uuid, Array


class Device(ComplexModel):
    '''
    class represent a device/electronics
    '''
    _type_info = [
        ('mrid', Uuid),
        ('name', Unicode),
    ]

    def __init__(self, mrid, name):
        super().__init__()
        self.mrid = mrid
        self.name = name

    def __json__(self):
        return json.dumps({"mrid": self.mrid,
                           "name": self.name})


class SynchronousMachine(Device):
    _type_info = [
        ('bus', Unicode),
        ('ratedS', Unicode),
        ('ratedU', Unicode),
        ('p', Unicode),
        ('q', Unicode),
        ('fdrid', Unicode),
        ('phases', Unicode),
    ]

    def __init__(self, name, bus, ratedS, ratedU, p, q, id, fdrid, phases):
        super().__init__(id, name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.fdrid = fdrid
        self.phases = phases


class Solar(Device):
    _type_info = [
        ('bus', Unicode),
        ('ratedS', Unicode),
        ('ratedU', Unicode),
        ('p', Unicode),
        ('q', Unicode),
        ('fdrid', Unicode),
        ('ipu', Unicode),
        ('phases', Unicode),
    ]

    def __init__(self, name, bus, ratedS, ratedU, ipu, p, q, id, fdrid, phases):
        super().__init__(id, name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.fdrid = fdrid
        self.phases = phases
        self.ipu = ipu


class Battery(Device):
    _type_info = [
        ('bus', Unicode),
        ('ratedS', Unicode),
        ('ratedU', Unicode),
        ('p', Unicode),
        ('q', Unicode),
        ('ipu', Unicode),
        ('phases', Unicode),
        ('ratedE', Unicode),
        ('storedE', Unicode),
        ('state', Unicode),
        ('fdrid', Unicode),
    ]

    def __init__(self, name, bus, ratedS, ratedU, ipu, ratedE, storedE, state, p, q, id, fdrid, phases):
        super().__init__(id, name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.fdrid = fdrid
        self.phases = phases
        self.ipu = ipu
        self.ratedE = ratedE
        self.storedE = storedE
        self.state = state


class Devices(ComplexModel):
    _type_info = [
        ('synchronousMachines', Array(SynchronousMachine)),
        ('solars', Array(Solar)),
        ('batterys', Array(Battery)),
    ]

    def __init__(self, synchronousMachines, solars, batterys):
        super().__init__()
        self.synchronousMachines = synchronousMachines
        self.solars = solars
        self.batterys = batterys


