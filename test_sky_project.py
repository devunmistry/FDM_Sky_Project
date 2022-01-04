from unittest import mock, TestCase

from ncclient.transport.errors import SSHError

from sky_project import Router

class TestConfigureLoopback(TestCase):
    def setUp(self):
        self.router = Router()

    def test_Router_createsRouterObject_whenRouterObjectInstantiated(self):
        result = isinstance(self.router, Router)
        assert result == True

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouter_101(self):
        with mock.patch("sky_project.manager") as mocked_manager: #at instance where sky_project.manager called, replaced with mock_manager
            self.router.configure_loopback("192.168.0.101", "830", "cisco", "cisco")
            result = mocked_manager.connect_ssh.assert_called_once_with(
                host='192.168.0.101',
                port='830',
                username='cisco',
                password='cisco',
                hostkey_verify=False,
                device_params={'name': 'csr'}) #asserts if mocked_manager.connect_ssh called with correct arguements
            assert result == None

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouter_102(self):
        with mock.patch("sky_project.manager") as mocked_manager:
            self.router.configure_loopback("192.168.0.102", "830", "router", "router")
            mocked_manager.connect_ssh.assert_called_once_with(
                host='192.168.0.102',
                port='830',
                username='router',
                password='router',
                hostkey_verify=False,
                device_params={'name': 'csr'})

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidIPAddressOrPort(self):
        self.assertRaisesRegex(
            SSHError,
            "Invalid IP address and/or port number",
            self.router.configure_loopback,
            "192.168.0.100", "830", "cisco", "cisco")

        self.assertRaisesRegex(
            SSHError,
            "Invalid IP address and/or port number",
            self.router.configure_loopback,
            "192.168.0.101", "800", "cisco", "cisco")