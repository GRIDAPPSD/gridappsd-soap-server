import unittest
import mock
import server, equipment


class ServerTestCase(unittest.TestCase):

    @mock.patch('server.group')
    @mock.patch('server.list_devices')
    @mock.patch('server.render_template')
    @mock.patch('server.derms_client')
    # @mock.patch('server.request')
    def test_create_group_html(self, mock_derms_client, mock_teamplate, mock_get_devices, mock_group):
        mock_teamplate.return_value = 'true'

        # mock_request.method = 'GET'
        server.deviceList = [equipment.Equipment('name', 'mrid')]
        with server.app.test_request_context("/create_group"):
            server.create_group_html()
        self.assertFalse(mock_derms_client.create_groups.called, "No group should have been created.")

        server.deviceList = []
        mock_get_devices.return_value = [equipment.Equipment('name', 'mrid')]
        with server.app.test_request_context("/create_group"):
            server.create_group_html()
        self.assertFalse(mock_derms_client.create_groups.called, "No group should have been created.")
        # mock_get_devices.assert_called_once()
        # self.assertTrue(mock_get_devices.called, "Failed to call get_devices().")

        # self.assertFalse(mock_get_devices.called, "Failed.")
        # mock_request.method = 'POST'
        # mock_request.form.get.return_value = '1'
        # mock_request.form.getlist.return_value = 'mock_device'
        mock_group_list = [mock_group.Group('1', '1', 'mock_device')]

        with server.app.test_request_context("/create_group", method="POST", data={'number_of_groups': 1, }):
            server.create_group_html()
        self.assertTrue(mock_derms_client.create_groups.called, "Failed to create group.")
        mock_derms_client.create_groups.assert_called_with(mock_group_list)
        # self.assertTrue(mock_get_devices.called, "Failed to call get_devices().")
        # self.assertEqual(mock_get_devices.call_count, 2)
        # mock_get_devices.assert_called_once()

        server.deviceList = [equipment.Equipment('name', 'mrid')]
        mock_get_devices.reset_mock()
        with server.app.test_request_context("/create_group"):
            server.create_group_html()
        self.assertTrue(mock_derms_client.create_groups.called, "Failed to create group.")
        mock_derms_client.create_groups.assert_called_with(mock_group_list)
        self.assertFalse(mock_get_devices.called, "Failed to call get_devices().")

        mock_derms_client.create_groups.return_value.Reply.Result = 'OK'
        with server.app.test_request_context("/create_group", method="POST", data={'number_of_groups': 1, }):
            server.create_group_html()
        self.assertTrue(mock_group.add_groups.called, "Failed to create group.")
        mock_group.add_groups.assert_called_with(mock_group_list)
        # self.assertFalse(mock_get_devices.called, "Failed to call get_devices().")

    # @mock.patch('dermsapp.server.derms_client.get_devices')
    @mock.patch('server.derms_client')
    def test_list_devices(self, mock_derms_client):
        # server.deviceList = ['test']
        # with server.app.test_request_context("/list_devices"):
        #     server.list_devices()
        # # assert not mock_derms_client.get_devices.called, "List devices already populated"
        # # assert mock_derms_client.get_devices.called == False, "List devices already populated"
        # self.assertFalse(mock_derms_client.get_devices.called, "List devices already populated")

        server.deviceList = []
        mock_derms_client.get_devices.return_value = [equipment.Equipment('name', 'mrid')]
        with server.app.test_request_context("/list_devices"):
            server.list_devices()
        self.assertTrue(mock_derms_client.get_devices.called, "Failed to load devices")
        assert len(server.deviceList) == 1
        assert server.deviceList[0].name == 'mrid'
        assert server.deviceList[0].mrid == 'name'
        # self.assertTrue(mock_get_devices.called, "Failed.")
        # self.assertEqual(True, False)
        # mock_get_devices.assert_called_once()


if __name__ == '__main__':
    unittest.main()
