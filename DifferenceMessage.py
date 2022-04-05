from spyne import ComplexModel, Unicode, Integer, Uuid, Array, DateTime, Boolean, Decimal, XmlAttribute, XmlData, Float


class OBJECT_DICT(ComplexModel):
    _type_info = [
        ('object', Unicode),
        ('attribute', Unicode),
        ('value', float)
    ]

    def __init__(self, Object=None, Attribute=None, Value=None, **kwargs):
        super().__init__(object = Object, attribute = Attribute, value = Value, **kwargs)
        self.object = Object
        self.attribute = Attribute
        self.value = Value

class MESSAGE(ComplexModel):
    _type_info = [
        ('timestamp', Unicode),
        ('difference_mrid', Unicode),
        ('reverse_differences', OBJECT_DICT.customize(max_occurs="unbounded", min_occurs=1)),
        ('forward_differences', OBJECT_DICT.customize(max_occurs="unbounded", min_occurs=1))
    ]

    def __init__(self, Timestamp=None, Difference_mrid=None, Reverse_differences=None, Forward_differences=None, **kwargs):
        super().__init__(timestamp = Timestamp, difference_mrid = Difference_mrid, reverse_differences = Reverse_differences, forward_differences = Forward_differences, **kwargs)
        self.timestamp = Timestamp
        self.difference_mrid = Difference_mrid
        if Reverse_differences is None:
            self.reverse_differences = []
        else:
            self.reverse_differences = Reverse_differences
        if Forward_differences is None:
            self.forward_differences = []
        else:
            self.forward_differences = Forward_differences


class INPUT(ComplexModel):
    _type_info = [
        ('simulation_id', Unicode),
        ('message', MESSAGE),
    ]

    def __init__(self, Simulation_id=None, Message=None, **kwargs):
        super().__init__(simulation_id=Simulation_id, message=Message, **kwargs)
        self.simulation_id = Simulation_id
        self.message = Message


class DIFFERENCEMESSAGE(ComplexModel):
    _type_info = [
        ('command', Unicode),
        ('input', INPUT),
    ]

    def __init__(self, Command=None, Input=None, **kwargs):
        super().__init__(command=Command, input=Input, **kwargs)
        self.command = Command
        self.input = Input