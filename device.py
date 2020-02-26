from spyne import ComplexModel, Unicode, Iterable, Uuid, Array, Boolean


class Device(ComplexModel):
    '''
    represents an end device
    '''
    __type_name__ = 'mRID'
    _type_info = [
        ('mRID', Unicode),  # XmlData(Uuid)
        ('name', Unicode),
        ('isSmartInverter', Boolean),
        ('usagePoint', Unicode)
    ]

    def __init__(self, mRID=None, name=None, isSmartInverter=None, usagePoint=None, **kwargs):
        super().__init__(mRID=mRID, name=name, isSmartInverter=isSmartInverter, usagePoint=usagePoint, **kwargs)
        self.mRID = mRID
        self.name = name
        self.isSmartInverter = isSmartInverter
        self.usagePoint = usagePoint