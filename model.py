from spyne import ComplexModel, Unicode, Iterable, Uuid, Array, Boolean
import jsons,json


class Model(ComplexModel):
    '''
    represents a model/container/feeder
    '''
    _type_info = [
        ('mRID', Unicode),  # XmlData(Uuid)
        ('name', Unicode)
    ]

    def __init__(self, mRID=None, name=None, **kwargs):
        super().__init__(mRID=mRID, name=name, **kwargs)
        self.mRID = mRID
        self.name = name


