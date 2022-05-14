import json


class Equipment(object):
    '''
    class represent a device/electronics
    '''
    def __init__(self, mrid=None, name=None):
        self.mrid = mrid
        self.name = name

    def __json__(self):
        return json.dumps({"mrid": self.mrid,
                           "name": self.name})


class SynchronousMachine(Equipment):
    def __init__(self, name, bus, ratedS, ratedU, p, q, id, fdrid, phases):
        super().__init__(mrid=fdrid, name=name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.id = id
        self.phases = phases


class Solar(Equipment):
    def __init__(self, name, bus, ratedS, ratedU, ipu, p, q, fdrid, phases):
        super().__init__(mrid=fdrid, name=name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.id = id
        self.phases = phases
        self.ipu = ipu


class Battery(Equipment):
    def __init__(self, name, bus, ratedS, ratedU, ipu, ratedE, storedE, state, p, q, id, fdrid, phases):
        super().__init__(mrid=fdrid, name=name)
        self.bus = bus
        self.ratedS = ratedS
        self.ratedU = ratedU
        self.p = p
        self.q = q
        self.id = id
        self.phases = phases
        self.ipu = ipu
        self.ratedE = ratedE
        self.storedE = storedE
        self.state = state


devices = []


# def get_devices():
#     with open("devices_list.json") as fp:
#         loaded_json = json.loads(fp.read())
#
#     devices_list = []
#
#     for x in loaded_json['devices']:
#         devices_list.append(Device(x['mrid'], x['name']))
#
#     if not devices:
#         for device in devices_list:
#             devices.append(device)
#
#     return devices


# def get_devices_json():
#     lst = get_devices()
#     return json.dumps([x.__dict__ for x in lst], indent=2)


# if __name__ == '__main__':
    # devices = get_devices()
    # for x in devices:
    #     print(x.__dict__)
    #
    # print(get_devices_json())