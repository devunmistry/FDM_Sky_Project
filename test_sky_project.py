from unittest import mock, TestCase

from sky_project import Router

class TestConfigureLoopback(TestCase):

    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco")
        self.router_b = Router("192.168.0.102", 830, "router", "router")

    def test_Router_createsRouterObject_whenRouterObjectInstantiated(self):
        result = isinstance(self.router_a, Router)
        assert result == True

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouterA(self):
        with mock.patch("sky_project.manager") as mocked_manager: #at instance where sky_project.manager called, replaced with mock_manager
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            result = mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.101',
                port = 830,
                username = 'cisco',
                password = 'cisco',
                hostkey_verify = False,
                device_params = {'name': 'csr'}) #asserts if mocked_manager.connect_ssh called with correct arguements
            assert result == None

    def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouterB(self):
        with mock.patch("sky_project.manager") as mocked_manager:
            self.router_b.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.102',
                port = 830,
                username = 'router',
                password = 'router',
                hostkey_verify = False,
                device_params = {'name': 'csr'})

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidIPAddress(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.host = "invalid"
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for router socket")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidPort(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.port = "invalid"
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid port for router socket")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnectionIPAddress(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.host = "192.168.0.100"
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.100:830 - could be incorrect ip address and/or port number")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnectionPort(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.port = 800
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.101:800 - could be incorrect ip address and/or port number")
   
    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectUsername(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.username = "incorrect"
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectPassword(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.password = "incorrect"
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password")

    def test_configureLoopback_callsEditConfig_whenConfigureLoopbackCalledRouterALoopback1(self):
        with mock.patch("sky_project.manager.connect_ssh") as mocked_connect_ssh:
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
            
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

    def test_configureLoopback_callsEditConfig_whenConfigureLoopbackCalledRouterBLoopback2(self):
        with mock.patch("sky_project.manager.connect_ssh") as mocked_connect_ssh:
            self.router_b.configure_loopback(2, "192.168.1.2", "255.255.255.0")
            
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

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidTextLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback("invalid", "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid id for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(-1, "192.168.1.1", "255.255.255.0")
            mocked_print.assert_called_once_with("Invalid id for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidTextLoopbackIP(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "invalid", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackIP(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "192.168.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid ip address for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidTextLoopbackSubnet(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "192.168.1.1", "invalid")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid subnet mask for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackSubnet(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255")
            mocked_print.assert_called_once_with("<class 'ValueError'>: Invalid subnet mask for loopback interface")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectLoopbackIPAddress(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "192.168.0.1", "255.255.255.0")
            mocked_print.assert_called_once_with("<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask")

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectLoopbackSubnet(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.2")
            mocked_print.assert_called_once_with("<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask")

class TestDeleteLoopback(TestCase):

    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco")

    def test_deleteLoopback_callsNcclientManagerConnectssh_whenDeleteLoopbackCalledRouterA(self):
        with mock.patch("sky_project.manager") as mocked_manager:
            self.router_a.delete_loopback(1)
            mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.101',
                port = 830,
                username = 'cisco',
                password = 'cisco',
                hostkey_verify = False,
                device_params = {'name': 'csr'})

    def test_deleteLoopback_callsEditConfig_whenDeleteLoopbackCalledRouterALoopback1(self):
        with mock.patch("ncclient.manager.connect_ssh") as mocked_connect_ssh:
            self.router_a.delete_loopback(1)

            conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback operation="delete">
                <name>1</name>
            </Loopback>
        </interface>
    </native>
</config>
"""
            edit_config_call = [mock.call().__enter__().edit_config(target = "running", config = conf, default_operation="merge")]
            mocked_connect_ssh.assert_has_calls(edit_config_call)

    def test_deleteLoopback_callsEditConfig_whenDeleteLoopbackCalledRouterALoopback2(self):
        with mock.patch("ncclient.manager.connect_ssh") as mocked_connect_ssh:
            self.router_a.delete_loopback(2)

            conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback operation="delete">
                <name>2</name>
            </Loopback>
        </interface>
    </native>
</config>
"""
            edit_config_call = [mock.call().__enter__().edit_config(target = "running", config = conf, default_operation="merge")]
            mocked_connect_ssh.assert_has_calls(edit_config_call)

    def test_deleteLoopback_handlesException_whenDeleteLoopbackCalledWithInvalidTextLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.delete_loopback("one")
            mocked_print.assert_called_once_with("Invalid id for loopback interface")
    
    def test_deleteLoopback_handlesException_whenDeleteLoopbackCalledWithInvalidNumLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.delete_loopback(-1)
            mocked_print.assert_called_once_with("Invalid id for loopback interface")

    def test_deleteLoopback_handlesException_whenDeleteLoopbackCalledNonExistentLoopbackID(self):
        with mock.patch("builtins.print") as mocked_print:
            self.router_a.delete_loopback(2)
            mocked_print.assert_called_once_with("<class 'ncclient.operations.rpc.RPCError'>: Interface deletion error - loopback id may not correspond with existing loopback interface")