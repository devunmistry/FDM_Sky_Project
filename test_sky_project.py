from unittest import mock, TestCase

from sky_project import Router

class TestConfigureLoopback(TestCase):

    def setUp(self):
        self.router = Router()

    def test_Router_createsRouterObject_whenRouterObjectInstantiated(self):
        result = isinstance(self.router, Router)
        assert result == True

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRA(self):
        with mock.patch("sky_project.manager") as mocked_manager: #at instance where sky_project.manager called, replaced with mock_manager
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            result = mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.101',
                port = 830,
                username = 'cisco',
                password = 'cisco',
                hostkey_verify = False,
                device_params = {'name': 'csr'}) #asserts if mocked_manager.connect_ssh called with correct arguements
            assert result == None

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRB(self):
        with mock.patch("sky_project.manager") as mocked_manager:
            self.router.configure_loopback("192.168.0.102", 830, "router", "router", 1, "192.168.1.1", "255.255.255.0")
            mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.102',
                port = 830,
                username = 'router',
                password = 'router',
                hostkey_verify = False,
                device_params = {'name': 'csr'})

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidIPAddressOrPort(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("invalid", 830, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for router socket")
        
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", "invalid", "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid port for router socket")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnection(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.100", 830, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.100:830 - could be incorrect ip address and/or port number")

        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 800, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.101:800 - could be incorrect ip address and/or port number")
   
    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectUsernameOrPassword(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "incorrect", "cisco", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password")

        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "incorrect", 1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password")

    def test_configureLoopback_callsEditConfig_whenConfigureLoopbackCalledRouter101Loopback1(self):
        with mock.patch("sky_project.manager.connect_ssh") as mocked_connect_ssh:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.0")
            
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
            mocked_connect_ssh.assert_has_calls(edit_config_call)

    def test_configureLoopback_callsEditConfig_whenConfigureLoopbackCalledRouter102Loopback2(self):
        with mock.patch("sky_project.manager.connect_ssh") as mocked_connect_ssh:
            self.router.configure_loopback("192.168.0.102", 830, "router", "router", 2, "192.168.1.2", "255.255.255.0")
            
            conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>2</name>
                <ip>
                    <address>
                        <primary>
                            <address>192.168.1.2</address>
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
            mocked_connect_ssh.assert_has_calls(edit_config_call)

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", "invalid", "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid id for loopback interface")

        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", -1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid id for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidLoopbackIP(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "invalid", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for loopback interface")

        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "192.168.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectLoopbackIPAddressOrSubnet(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "192.168.0.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask")

        with mock.patch("builtins.print") as mocked_print:
            self.router.configure_loopback("192.168.0.101", 830, "cisco", "cisco", 1, "192.168.1.1", "255.255.255.2")
            mocked_print.assert_called_once_with("<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask")

class TestDeleteLoopback(TestCase):

    def test_deleteLoopback_callsNcclientManagerConnectssh_whenDeleteLoopbackCalledRA(self):
        router = Router()
        with mock.patch("sky_project.manager") as mocked_manager:
            router.delete_loopback()
            mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.101',
                port = 830,
                username = 'cisco',
                password = 'cisco',
                hostkey_verify = False,
                device_params = {'name': 'csr'})