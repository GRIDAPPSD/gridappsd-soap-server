from spyne import ComplexModel, Unicode, Boolean, Uuid


class Device(ComplexModel):
    '''
    represents an end device
    '''
    _type_info = [
        ('mRID', Uuid.customize(max_occurs=1, min_occurs=1)),  # XmlData(Uuid)
        ('name', Unicode.customize(max_occurs=1, min_occurs=1)),
        ('isSmartInverter', Boolean),
        ('usagePoint', Unicode.customize(max_occurs=1, min_occurs=1))
    ]

    def __init__(self, mRID=None, name=None, isSmartInverter=None, usagePoint=None, **kwargs):
        super().__init__(mRID=mRID, name=name, isSmartInverter=isSmartInverter, usagePoint=usagePoint, **kwargs)
        self.mRID = mRID
        self.name = name
        self.isSmartInverter = isSmartInverter
        self.usagePoint = usagePoint

    # def __json__(self):
    #     return json.dumps({"mRID": self.mRID,
    #                        "name": self.name,
    #                        "isSmartInverter": self.isSmartInverter,
    #                        "usagePoint": self.usagePoint})