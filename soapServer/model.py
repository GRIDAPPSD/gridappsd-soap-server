from spyne import ComplexModel, Unicode, Uuid


class Model(ComplexModel):
    '''
    represents a model/container/feeder
    '''
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=1)),  # XmlData(Uuid)
        ('name', Unicode.customize(max_occurs=1, min_occurs=1))
    ]

    def __init__(self, mRID=None, name=None, **kwargs):
        super().__init__(mRID=mRID, name=name, **kwargs)
        self.mRID = mRID
        self.name = name


class ModelArray(ComplexModel):
    Models = Model.customize(max_occurs='unbounded')