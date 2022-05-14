import datetime
import unittest
import mock
# import soapServer
# import pytest
import soap_server
from soap_server import DERGroupsPayloadType, HeaderType, EndDeviceGroup, DERFunction, Version, EndDevice, Name, DERGroups
from message import VerbType, ResultType, LevelType
# @mock.patch('soapServer.conn')
mock_GridAPPSD = mock.MagicMock()
soap_server.conn = mock_GridAPPSD

# @pytest.fixture(scope="module", autouse=True)
# def mock_GridAPPSD(mocker):
#     return mocker.patch('soapServer.GridAPPSD', autospec=True)


# # @pytest.mark.usefixtures("mock_GridAPPSD")
# class SoapServerTestCase(unittest.TestCase):
#     # @mock.patch('soapServer.GridAPPSD', autospec=True)
#     # def setUp(self):
#     #     self.mock_GridAPPSD = mock.patch.object(
#     #         soapServer, 'conn', return_value=GridAPPSD()
#     #     )
#     # @mock.patch('soapServer.GridAPPSD', autospec=True)
#     def test_get_DERM_devices(self):
#         mock_GridAPPSD.reset_mock()
#         mock_GridAPPSD.query_data.return_value = 'query_results'
#         soap_server.get_DERM_devices()
#         self.assertEqual(mock_GridAPPSD.query_data.call_count, 3)

# @mock.patch('soapServer.conn')

class GetDevicesServiceTestCase(unittest.TestCase):
    def test_GetDevices(self):
        mock_GridAPPSD.reset_mock()
        # sol = {'name': {'type': 'literal', 'value': '3p_existi'}, 'bus': {'type': 'literal', 'value': 'b4832_sec'}, 'ratedS': {'type': 'literal', 'value': '209000'}, 'ratedU': {'type': 'literal', 'value': '416'}, 'ipu': {'type': 'literal', 'value': '1.1111111'}, 'p': {'type': 'literal', 'value': '1'}, 'q': {'type': 'literal', 'value': '0'}, 'id': {'type': 'literal', 'value': '00A69D4E-EB07-4AF7-8C93-BA7A3924B07A'}, 'fdrid': {'type': 'literal', 'value': '67AB291F-DCCD-31B7-B499-338206B9828F'}, 'phases': {'type': 'literal', 'value': ''}, 'ratedE': {'type': 'literal', 'value': '500000'}, 'storedE': {'type': 'literal', 'value': '500000'}, 'state': {'type': 'literal', 'value': 'Waiting'}}
        # bat = {'name': {'type': 'literal', 'value': 'battery16'}, 'bus': {'type': 'literal', 'value': 'm2001-ess'}, 'ratedS': {'type': 'literal', 'value': '250000'}, 'ratedU': {'type': 'literal', 'value': '124'}, 'ipu': {'type': 'literal', 'value': '1.1111111'}, 'p': {'type': 'literal', 'value': '0'}, 'q': {'type': 'literal', 'value': '0'}, 'id': {'type': 'literal', 'value': 'C138DF63-68E1-4B3C-B280-55E210D4E9FE'}, 'fdrid': {'type': 'literal', 'value': 'AAE94E4A-2465-6F5E-37B1-3E72183A4E44'}, 'phases': {'type': 'literal', 'value': ''}, 'ratedE': {'type': 'literal', 'value': '500000'}, 'storedE': {'type': 'literal', 'value': '500000'}, 'state': {'type': 'literal', 'value': 'Waiting'}}
        mock_GridAPPSD.query_data.return_value = {'data':
                   {'head': {'vars': ['name', 'bus', 'ratedS', 'ratedU', 'ipu', 'ratedE', 'storedE', 'state', 'p', 'q', 'id', 'fdrid', 'phases']},
                    'results': {'bindings': [
                        {'name': {'type': 'literal', 'value': 'endDevice_Bat_WTG'}, 'mrid': {'type': 'literal', 'value': 'a1321228-40ee-4eb6-86a1-2c7c6a642fc4'}, 'issmart': {'type': 'literal', 'value': 'True'}, 'upoint': {'type': 'literal', 'value': 'f9e17abf-babf-466b-8253-86161f0b95da'}},
                        {'name': {'type': 'literal', 'value': 'endDevice_PV_1'}, 'mrid': {'type': 'literal', 'value': '99491fc0-44ad-482f-9319-72c651c0ef5f'}, 'issmart': {'type': 'literal', 'value': 'True'}, 'upoint': {'type': 'literal', 'value': '11345f6b-f706-4c43-957c-ba88a44890bb'}},
                        {'name': {'type': 'literal', 'value': 'endDevice_Rooftop_1'}, 'mrid': {'type': 'literal', 'value': 'd79490ce-a5c1-470c-af3a-93ffdc1944ff'}, 'issmart': {'type': 'literal', 'value': 'True'}, 'upoint': {'type': 'literal', 'value': '58aa7600-fc5e-4753-ab7d-654cb33d2b73'}}]}},
               'responseComplete': True,
               'id': '861322400'}
        real = soap_server.GetDevicesService()
        value = real.GetDevices(None)
        assert len(value) == 3
        assert value[0].name == 'endDevice_Bat_WTG'
        assert value[0].mRID == 'a1321228-40ee-4eb6-86a1-2c7c6a642fc4'
        assert value[0].isSmartInverter == True
        self.assertEqual(mock_GridAPPSD.query_data.call_count, 1)


class CreateDERGroupsServiceTestCase(unittest.TestCase):
    def test_CreateDERGroups(self):
        header = HeaderType(verb=VerbType.CREATE, noun='DERGroups', timestamp=datetime.datetime.now(), messageID='360150a8-4d74-4cd2-8628-79dafc8ac6c1', correlationID='57a597c0-7d74-4796-9bb5-434c9250ddf0')
        # payload = DERGroupsPayloadType(DERGroups=[EndDeviceGroup(mRID='a6af4a25-878e-4703-8bdf-7245dffe67f2', description='1', DERFunction=DERFunction(connectDisconnect=True, frequencyWattCurveFunction=False, maxRealPowerLimiting=False, rampRateControl=False, reactivePowerDispatch=False, realPowerDispatch=True, voltageRegulation=False, voltVarCurveFunction=False, voltWattCurveFunction=False), endDevices=[EndDevice(mRID='99decc0d-6d70-48d6-8e63-a9ee6ccf1514'), EndDevice(mRID='1f2dd132-00b5-4979-9338-75aada4fb80a')], names=[Name(name='1')], version=Version(date=datetime.datetime.now(), major=1, minor=0, revision=0))])
        payload = DERGroupsPayloadType(DERGroups=DERGroups(endDeviceGroup=[EndDeviceGroup(mRID='ff329fde-6a06-4c91-af1f-b321d8b629e1', description='test2', DERFunction=DERFunction(connectDisconnect=False, frequencyWattCurveFunction=False, maxRealPowerLimiting=False, rampRateControl=False, reactivePowerDispatch=False, realPowerDispatch=True, voltageRegulation=False, voltVarCurveFunction=False, voltWattCurveFunction=False), endDevices=[EndDevice(mRID='7357f5b6-86de-49b5-9e3c-42707475ab41'), EndDevice(mRID='a1321228-40ee-4eb6-86a1-2c7c6a642fc4')], names=[Name(name='group2')], version=Version(date=datetime.datetime.now(), major=1, minor=0, revision=0))]))
        # payload = Payload()
        real = soap_server.CreateDERGroupsService()
        value = real.CreateDERGroups(None, header, payload)
        assert value.Header.Verb == VerbType.REPLY
        assert value.Header.Noun == 'DERGroups'
        assert value.Reply.Error.code == '6.1'
        assert value.Reply.Error.level == LevelType.FATAL
        assert value.Reply.Error.reason == 'Request cancelled per business rule'
        assert value.Reply.Result == ResultType.FAILED
        # print(value)
        # self.assertEqual(True, False)


# import os
#
# @mock.patch("os.listdir")
# class Test(unittest.TestCase):
#
#     def test_not_decorated_and_not_tested(self, mock_listdir):
#         soapServer.get_DERM_devices()
#
#     def test3(self, mock_listdir):
#         mock_listdir.return_value = "test3"
#         assert  "test3" == os.listdir()


if __name__ == '__main__':
    unittest.main()
