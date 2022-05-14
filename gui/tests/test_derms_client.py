import datetime
import unittest, pytest
from uuid import UUID

import mock
import derms_client, equipment, group


class DermsClientTestCase(unittest.TestCase):
    # @pytest.fixture  # With pytest-mock
    # def mock_zeep_client(mocker):
    #     return mocker.patch('dermsapp.derms_client.Client')
    #
    # @pytest.fixture
    # def mock_etree(mocker):
    #     return mocker.patch('dermsapp.derms_client.etree')
    #
    # @pytest.fixture
    # def mock_history_plugin(mocker):
    #     return mocker.patch('dermsapp.derms_client.HistoryPlugin')

    @mock.patch('derms_client.HistoryPlugin')
    @mock.patch('derms_client.etree')
    @mock.patch('derms_client.Client', autospec=True)
    def test_get_devices(self, mock_zeep_client, mock_etree, mock_history_plugin):
        instance = mock_zeep_client.return_value
        instance.service.GetDevices.return_value.synchronousMachines.SynchronousMachine = ["SynchronousMachine"]
        instance.service.GetDevices.return_value.solars.Solar = ["Solar"]
        instance.service.GetDevices.return_value.batteries.Battery = ["Battery"]
        # mock_zeep_client.return_value = mock_zeep_client
        # mock_zeep_client.service.GetDevices.return_value.synchronousMachines.SynchronousMachine = ["SynchronousMachine"]
        # mock_zeep_client.service.GetDevices.return_value.solars.Solar = ["Solar"]
        # mock_zeep_client.service.GetDevices.return_value.batteries.Battery = ["Battery"]

        mock_etree.tounicode.return_value = 'envelope'
        mock_history_plugin.last_sent['envelope'] = 'last_sent_envelope'
        mock_history_plugin.last_received['envelope'] = 'last_received_envelope'

        value = derms_client.get_devices()
        self.assertTrue(instance.service.GetDevices.called, "Failed to call GetDevices().")
        # self.assertTrue(mock_zeep_client.service.GetDevices.called, "Failed to call GetDevices().")
        assert value.batteries.Battery == ["Battery"]
        assert value.solars.Solar == ["Solar"]
        assert value.synchronousMachines.SynchronousMachine == ["SynchronousMachine"]

    # @mock.patch('derms_client.datetime')
    # @mock.patch('derms_client.uuid')
    # @mock.patch('derms_client.get_service')
    # @mock.patch('derms_client.HistoryPlugin')
    # @mock.patch('derms_client.etree')
    # @mock.patch('derms_client.Client', autospec=True)
    # def test_create_group(self, mock_zeep_client, mock_etree, mock_history_plugin, mock_get_service, mock_uuid, mock_datetime):
    #     mock_etree.tounicode.return_value = 'envelope'
    #     mock_history_plugin.last_sent['envelope'] = 'last_sent_envelope'
    #     mock_history_plugin.last_received['envelope'] = 'last_received_envelope'
    #     mock_uuid.uuid4.return_value = 'uuid4'
    #     mock_datetime.datetime.now.return_value = 'datetime_now'
    #
    #     mrid = 'mrid'
    #     name = 'name'
    #     device_mrid_list = ['device_mrid']
    #
    #     headers = {'Verb': 'create',
    #                'Noun': 'DERGroups',
    #                'Timestamp': 'datetime_now',
    #                'MessageID': 'uuid4',
    #                'CorrelationID': 'uuid4'}
    #     body = {'DERGroups': [{'EndDeviceGroup': {'mRID': 'mrid',
    #                                               'description': 'name',
    #                                               'DERFunction': {'connectDisconnect': 'true',
    #                                                               'frequencyWattCurveFunction': 'false',
    #                                                               'maxRealPowerLimiting': 'false',
    #                                                               'rampRateControl': 'false',
    #                                                               'reactivePowerDispatch': 'false',
    #                                                               'voltageRegulation': 'false',
    #                                                               'realPowerDispatch': 'true',
    #                                                               'voltVarCurveFunction': 'false',
    #                                                               'voltWattCurveFunction': 'false'},
    #                                               'EndDevices': [{'mRID': 'device_mrid'}],
    #                                               'Names': [{'name': 'name'}],
    #                                               'version': {'date': '2017-05-31T13:55:01-06:00',
    #                                                           'major': 1,
    #                                                           'minor': 0,
    #                                                           'revision': 0}
    #                                               }
    #                            }]
    #             }
    #
    #     value = derms_client.create_groups(mrid, name, 'test', device_mrid_list)
    #
    #     self.assertTrue(mock_get_service.called, "Failed to call get_service().")
    #     mock_get_service.assert_called_once_with(mock_zeep_client.return_value, "create")
    #     self.assertTrue(mock_get_service.return_value.CreateDERGroups.called, "Failed to call CreateDERGroups().")
    #     mock_get_service.return_value.CreateDERGroups.assert_called_once_with(Header=headers, Payload=body)

    @mock.patch('derms_client.uuid')
    def test__build_endpoint_header(self, mock_uuid):
        mock_uuid.uuid4.return_value = 'uuid4'
        verb = 'create'
        message_id = 'message_id'
        correlation_id = 'correlation_id'
        noun = "DERGroups"
        value = derms_client._build_endpoint_header(verb, noun)
        self.assertEqual(mock_uuid.uuid4.call_count, 2)


    def test__get_create_body(self):
        pass

    @mock.patch('derms_client.Client', autospec=True)
    def test_get_service(self, mock_zeep_client):
        verb = "CREATE"
        client = mock_zeep_client.return_value
        client.create_service.return_value = 'true'
        value = derms_client.get_service(client, verb)
        self.assertTrue(client.create_service.called, "Failed to call create_service")
        client.create_service.assert_called_with('{der.pnnl.gov}CreateDERGroupsService', 'http://127.0.0.1:8008/create/executeDERGroups')
        assert value == 'true'

    @mock.patch('derms_client.datetime')
    @mock.patch('derms_client.uuid')
    @mock.patch('derms_client.get_service')
    @mock.patch('derms_client.HistoryPlugin')
    @mock.patch('derms_client.etree')
    @mock.patch('derms_client.Client', autospec=True)
    def test_create_groups(self, mock_zeep_client, mock_etree, mock_history_plugin, mock_get_service, mock_uuid, mock_datetime):
        mock_etree.tounicode.return_value = 'envelope'
        mock_history_plugin.last_sent['envelope'] = 'last_sent_envelope'
        mock_history_plugin.last_received['envelope'] = 'last_received_envelope'
        mock_uuid.uuid4.return_value = 'uuid4'
        mock_datetime.datetime.now.return_value = 'datetime_now'

        device_mrid_list = ['device_mrid1', 'device_mrid2']
        derfunc = group.DERFunctions(connectDisconnect=True, frequencyWattCurveFunction=False, maxRealPowerLimiting=False,
                 rampRateControl=False, reactivePowerDispatch=False, realPowerDispatch=True, voltageRegulation=False,
                 voltVarCurveFunction=False, voltWattCurveFunction=False)
        group_list = [group.Group('group_mrid', 'group_name', 'group_name', device_mrid_list, derFunctions=derfunc)]

        headers = {'Verb': 'CREATE',
                   'Noun': 'DERGroups',
                   'Timestamp': 'datetime_now',
                   'MessageID': 'uuid4',
                   'CorrelationID': 'uuid4'}
        body = {'DERGroups': {'EndDeviceGroup': [{'mRID': 'group_mrid',
                                                  'description': 'group_name',
                                                  'DERFunction': {'connectDisconnect': 'true',
                                                                  'frequencyWattCurveFunction': 'false',
                                                                  'maxRealPowerLimiting': 'false',
                                                                  'rampRateControl': 'false',
                                                                  'reactivePowerDispatch': 'false',
                                                                  'voltageRegulation': 'false',
                                                                  'realPowerDispatch': 'true',
                                                                  'voltVarCurveFunction': 'false',
                                                                  'voltWattCurveFunction': 'false'},
                                                  'EndDevices': [{'mRID': 'device_mrid1'}, {'mRID': 'device_mrid2'}],
                                                  'Names': {'name': 'group_name'},
                                                  'version': {'date': '2017-05-31T13:55:01-06:00',
                                                              'major': 1,
                                                              'minor': 0,
                                                              'revision': 0}
                                                  }
                               ]}
                }
        value = derms_client.create_groups(group_list)
        self.assertTrue(mock_get_service.called, "Failed to call get_service().")
        mock_get_service.assert_called_once_with(mock_zeep_client.return_value, "CREATE")
        self.assertTrue(mock_get_service.return_value.CreateDERGroups.called, "Failed to call CreateDERGroups().")
        mock_get_service.return_value.CreateDERGroups.assert_called_once_with(Header=headers, Payload=body)


if __name__ == '__main__':
    unittest.main()
