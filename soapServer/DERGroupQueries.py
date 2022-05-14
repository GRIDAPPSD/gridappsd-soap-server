from spyne import Uuid, ComplexModel
from message import Name


class EndDeviceGroup(ComplexModel):
    """Abstraction for management of group communications within a two-way AMR
    system or the data for a group of related end devices. Commands can be
    issued to all of the end devices that belong to the group using a
    defined group address and the underlying AMR communication
    infrastructure. A DERGroup and a PANDeviceGroup is an
    EndDeviceGroup."""
    _type_info = [
        ('mRID', Uuid),
        ('Names', Name.customize(max_occurs="unbounded", min_occurs=0)),
    ]

    def __init__(self, mRID=None, names=None, **kwargs):
        super().__init__(mRID=mRID, Names=names, **kwargs)
        self.mRID = mRID
        if names is None:
            self.names = []
        else:
            self.names = names
# end class EndDeviceGroup


class DERGroupQueries(ComplexModel):
    _type_info = [
        ('EndDeviceGroup', EndDeviceGroup.customize(max_occurs="unbounded", min_occurs=1)),
    ]

    def __init__(self, endDeviceGroup=None, **kwargs):
        super().__init__(EndDeviceGroup=endDeviceGroup, **kwargs)
        if endDeviceGroup is None:
            self.endDeviceGroup = []
        else:
            self.endDeviceGroup = endDeviceGroup
# end class DERGroupQueries
