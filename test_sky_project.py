from unittest import mock, TestCase

from ncclient.transport.errors import AuthenticationError, SSHError
from socket import gaierror

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
        self.assertRaisesRegex( #invalid ip address
            gaierror,
            "Invalid IP address and/or port number",
            self.router.configure_loopback,
            "invalid", "830", "cisco", "cisco")

        self.assertRaisesRegex( #invalid port number
            gaierror,
            "Invalid IP address and/or port number",
            self.router.configure_loopback,
            "192.168.0.101", "invalid", "cisco", "cisco")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnection(self):
        self.assertRaisesRegex( #incorrect ip address
            SSHError,
            "Could not open socket 192.168.0.100:830 - could be incorrect IP address and/or port number",
            self.router.configure_loopback,
            "192.168.0.100", "830", "cisco", "cisco")

        self.assertRaisesRegex( #incorrect port number
            SSHError,
            "Could not open socket 192.168.0.101:800 - could be incorrect IP address and/or port number",
            self.router.configure_loopback,
            "192.168.0.101", "800", "cisco", "cisco")
    
    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectUsernameOrPassword(self):
        self.assertRaisesRegex( #incorrect username
            AuthenticationError,
            "Incorrect username and/or password",
            self.router.configure_loopback,
            "192.168.0.101", "830", "incorrect", "cisco")

        self.assertRaisesRegex( #incorrect password
            AuthenticationError,
            "Incorrect username and/or password",
            self.router.configure_loopback,
            "192.168.0.101", "830", "cisco", "incorrect")

    def test_configureLoopback_callsEditConfig_whenConfigureLoopbackCalledRouter101Loopback1(self):
        with mock.patch("sky_project.manager.connect_ssh") as mocked_edit_config:
            self.router.configure_loopback("192.168.0.101", "830", "cisco", "cisco")
            
            conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>1</name>
                <ip>
                    <address>
                        <primary>
                            <address>192.168.1.1</address>
                            <mask>255.255.255.0</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""
    
            edit_config_call = [mock.call().__enter__().edit_config(target = "running", config = conf, default_operation="merge")]
            mocked_edit_config.assert_has_calls(edit_config_call)
