import datetime
import unittest
import mock
import soap_server
import pytest
from DERGroups import Payload, Header, EndDeviceGroup, DERFunction, Version, EndDeviceType, NameType

# @mock.patch('soap_server.conn')
mock_GridAPPSD = mock.MagicMock()
soap_server.conn = mock_GridAPPSD

# @pytest.fixture(scope="module", autouse=True)
# def mock_GridAPPSD(mocker):
#     return mocker.patch('soap_server.GridAPPSD', autospec=True)


# @pytest.mark.usefixtures("mock_GridAPPSD")
class SoapServerTestCase(unittest.TestCase):
    # @mock.patch('soap_server.GridAPPSD', autospec=True)
    # def setUp(self):
    #     self.mock_GridAPPSD = mock.patch.object(
    #         soap_server, 'conn', return_value=GridAPPSD()
    #     )
    # @mock.patch('soap_server.GridAPPSD', autospec=True)
    def test_get_DERM_devices(self):
        mock_GridAPPSD.reset_mock()
        mock_GridAPPSD.query_data.return_value = 'query_results'
        soap_server.get_DERM_devices()
        self.assertEqual(mock_GridAPPSD.query_data.call_count, 3)

# @mock.patch('soap_server.conn')

class GetDevicesServiceTestCase(unittest.TestCase):
    def test_GetDevices(self):
        mock_GridAPPSD.reset_mock()
        # sol = {'name': {'type': 'literal', 'value': '3p_existi'}, 'bus': {'type': 'literal', 'value': 'b4832_sec'}, 'ratedS': {'type': 'literal', 'value': '209000'}, 'ratedU': {'type': 'literal', 'value': '416'}, 'ipu': {'type': 'literal', 'value': '1.1111111'}, 'p': {'type': 'literal', 'value': '1'}, 'q': {'type': 'literal', 'value': '0'}, 'id': {'type': 'literal', 'value': '00A69D4E-EB07-4AF7-8C93-BA7A3924B07A'}, 'fdrid': {'type': 'literal', 'value': '67AB291F-DCCD-31B7-B499-338206B9828F'}, 'phases': {'type': 'literal', 'value': ''}, 'ratedE': {'type': 'literal', 'value': '500000'}, 'storedE': {'type': 'literal', 'value': '500000'}, 'state': {'type': 'literal', 'value': 'Waiting'}}
        # bat = {'name': {'type': 'literal', 'value': 'battery16'}, 'bus': {'type': 'literal', 'value': 'm2001-ess'}, 'ratedS': {'type': 'literal', 'value': '250000'}, 'ratedU': {'type': 'literal', 'value': '124'}, 'ipu': {'type': 'literal', 'value': '1.1111111'}, 'p': {'type': 'literal', 'value': '0'}, 'q': {'type': 'literal', 'value': '0'}, 'id': {'type': 'literal', 'value': 'C138DF63-68E1-4B3C-B280-55E210D4E9FE'}, 'fdrid': {'type': 'literal', 'value': 'AAE94E4A-2465-6F5E-37B1-3E72183A4E44'}, 'phases': {'type': 'literal', 'value': ''}, 'ratedE': {'type': 'literal', 'value': '500000'}, 'storedE': {'type': 'literal', 'value': '500000'}, 'state': {'type': 'literal', 'value': 'Waiting'}}
        mock_GridAPPSD.query_data.return_value = {'data':
                   {'head': {'vars': ['name', 'bus', 'ratedS', 'ratedU', 'ipu', 'ratedE', 'storedE', 'state', 'p', 'q', 'id', 'fdrid', 'phases']},
                    'results': {'bindings': [{'name': {'type': 'literal', 'value': 'diesel590'}, 'bus': {'type': 'literal', 'value': 'm1089-die'}, 'ratedS': {'type': 'literal', 'value': '737000'}, 'ratedU': {'type': 'literal', 'value': '480'}, 'ipu': {'type': 'literal', 'value': '1.1111111'}, 'p': {'type': 'literal', 'value': '0'}, 'q': {'type': 'literal', 'value': '0'}, 'id': {'type': 'literal', 'value': '520CE479-D0A7-4C2D-A3E8-5728D22434B2'}, 'fdrid': {'type': 'literal', 'value': 'AAE94E4A-2465-6F5E-37B1-3E72183A4E44'}, 'phases': {'type': 'literal', 'value': ''}, 'ratedE': {'type': 'literal', 'value': '500000'}, 'storedE': {'type': 'literal', 'value': '500000'}, 'state': {'type': 'literal', 'value': 'Waiting'}}]}},
               'responseComplete': True,
               'id': '861322400'}
        real = soap_server.GetDevicesService()
        value = real.GetDevices(None)
        assert len(value.synchronousMachines) == 1
        assert value.synchronousMachines[0].name == 'diesel590'
        assert len(value.solars) == 1
        assert value.solars[0].bus == 'm1089-die'
        assert len(value.batteries) == 1
        assert value.batteries[0].ratedS == '737000'
        self.assertEqual(mock_GridAPPSD.query_data.call_count, 3)


class CreateDERGroupsServiceTestCase(unittest.TestCase):
    def test_CreateDERGroups(self):
        header = Header(Verb='create', Noun='DERGroups', Timestamp=datetime.datetime.now(), MessageID='360150a8-4d74-4cd2-8628-79dafc8ac6c1', CorrelationID='57a597c0-7d74-4796-9bb5-434c9250ddf0')
        payload = Payload(DERGroups=[EndDeviceGroup(mRID='a6af4a25-878e-4703-8bdf-7245dffe67f2', description='1', DERFunction=DERFunction(connectDisconnect=True, frequencyWattCurveFunction=False, maxRealPowerLimiting=False, rampRateControl=False, reactivePowerDispatch=False, realPowerDispatch=True, voltageRegulation=False, voltVarCurveFunction=False, voltWattCurveFunction=False), EndDevices=[EndDeviceType(mRID='99decc0d-6d70-48d6-8e63-a9ee6ccf1514'), EndDeviceType(mRID='1f2dd132-00b5-4979-9338-75aada4fb80a')], Names=[NameType(name='1')], version=Version(date=datetime.datetime.now(), major=1, minor=0, revision=0))])
        # payload = Payload()
        real = soap_server.CreateDERGroupsService()
        value = real.CreateDERGroups(None, header, payload)
        # self.assertEqual(True, False)


# import os
#
# @mock.patch("os.listdir")
# class Test(unittest.TestCase):
#
#     def test_not_decorated_and_not_tested(self, mock_listdir):
#         soap_server.get_DERM_devices()
#
#     def test3(self, mock_listdir):
#         mock_listdir.return_value = "test3"
#         assert  "test3" == os.listdir()


if __name__ == '__main__':
    unittest.main()
