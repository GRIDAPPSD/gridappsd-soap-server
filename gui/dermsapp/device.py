import json
class Device(object):
    '''
    represents an end device
    '''

    def __init__(self, mRID=None, name=None, isSmartInverter=None, usagePoint=None, **kwargs):
        self.mRID = mRID
        self.name = name
        self.isSmartInverter = isSmartInverter
        self.usagePoint = usagePoint

    # def __repr__(self):
    #     return jsons.dumps(self.__dict__)


# def get_devices():
#     with open("devices_list.json") as fp:
#         loaded_json = json.loads(fp.read())
#
#     devices_list = []
#
#     for x in loaded_json:
#         devices_list.append(Device(mRID=x['mRID'], name=x['name'], isSmartInverter=x['isSmartInverter'],
#                                    usagePoint=x['usagePoint']))
#     return devices_list