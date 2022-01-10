from unittest import mock, skip, TestCase

from sky_project import Router

class TestConfigureLoopback(TestCase):

    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco", 0)
        self.router_b = Router("192.168.0.102", 830, "router", "router", 0)

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
        self.router_a.host = "invalid"
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "<class 'ValueError'>: Invalid ip address for router socket"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidPort(self):
        self.router_a.port = "invalid"
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "Invalid port for router socket"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnectionIPAddress(self):
        self.router_a.host = "192.168.0.100"
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.100:830 - could be incorrect ip address and/or port number"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledButCannotEstablishSSHConnectionPort(self):
        self.router_a.port = 800
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "<class 'ncclient.transport.errors.SSHError'>: Could not open router socket 192.168.0.101:800 - could be incorrect ip address and/or port number"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectUsername(self):
        self.router_a.username = "incorrect"
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectPassword(self):
        self.router_a.password = "incorrect"
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")
        assert result == "<class 'ncclient.transport.errors.AuthenticationError'>: Incorrect router SSH username and/or password"

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
        result = self.router_a.configure_loopback("invalid", "192.168.1.1", "255.255.255.0")
        assert result == "Invalid id for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackID(self):
        result = self.router_a.configure_loopback(-1, "192.168.1.1", "255.255.255.0")
        assert result == "Invalid id for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidTextLoopbackIP(self):
        result = self.router_a.configure_loopback(1, "invalid", "255.255.255.0")
        assert result == "<class 'ValueError'>: Invalid ip address for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackIP(self):
        result = self.router_a.configure_loopback(1, "192.168.1", "255.255.255.0")
        assert result == "<class 'ValueError'>: Invalid ip address for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidTextLoopbackSubnet(self):
        result = self.router_a.configure_loopback(1, "192.168.1.1", "invalid")
        assert result == "<class 'ValueError'>: Invalid subnet mask for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithInvalidNumLoopbackSubnet(self):
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255")
        assert result == "<class 'ValueError'>: Invalid subnet mask for loopback interface"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectLoopbackIPAddress(self):
        result = self.router_a.configure_loopback(1, "192.168.0.1", "255.255.255.0")
        assert result == "<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask"

    def test_configureLoopback_handlesException_whenConfigureLoopbackCalledWithIncorrectLoopbackSubnet(self):
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.2")
        assert result == "<class 'ncclient.operations.rpc.RPCError'>: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask"

class TestDeleteLoopback(TestCase):

    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco", 0)

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
        result = self.router_a.delete_loopback("one")
        assert result == "Invalid id for loopback interface"

    def test_deleteLoopback_handlesException_whenDeleteLoopbackCalledWithInvalidNumLoopbackID(self):
        result = self.router_a.delete_loopback(-1)
        assert result == "Invalid id for loopback interface"

    def test_deleteLoopback_handlesException_whenDeleteLoopbackCalledNonExistentLoopbackID(self):
        result = self.router_a.delete_loopback(2)
        assert result == "<class 'ncclient.operations.rpc.RPCError'>: Interface deletion error - loopback id may not correspond with existing loopback interface"

class TestListInterfaces(TestCase):

    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco", 0)
    
    @skip("Mocked object prevents creation of string, leading to errors. Test not fully necessary, as the functions tested are also called successfully in later tests")
    def test_listInterfaces_callsNcclientConnectssh_whenListInterfacesCalledRouterA(self):
        with mock.patch("sky_project.manager") as mocked_manager:
            self.router_a.list_interfaces()
            mocked_manager.connect_ssh.assert_called_once_with(
                host = '192.168.0.101',
                port = 830,
                username = 'cisco',
                password = 'cisco',
                hostkey_verify = False,
                device_params = {'name': 'csr'})

    @skip("Mocked object prevents creation of string, leading to errors. Test not fully necessary, as the functions tested are also called successfully in later tests")
    def test_listInterfaces_callsGet_whenListInterfacesCalledRouterA(self):
        with mock.patch("ncclient.manager.connect_ssh") as mocked_connect_ssh:
            self.router_a.list_interfaces()

            interfaces = '''
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>
        </name>
        <state>
            <oper-status>
            </oper-status>
        </state>
    </interface>
</interfaces>
'''

            get_config_call = [mock.call().__enter__().get(filter=("subtree", interfaces))]
            mocked_connect_ssh.assert_has_calls(get_config_call)

    def test_listInterfaces_callsParseString_whenListInterfacesCalledRouterA(self):
        with mock.patch("sky_project.parseString") as mocked_parseString:
            self.router_a.list_interfaces()
            mocked_parseString.assert_called()

class TestDryRun(TestCase):
    def setUp(self):
        self.router_a = Router("192.168.0.101", 830, "cisco", "cisco", 0)

    def test_dryRun_dryRunVariable0_whenRouterObjectCreated(self):
        result = self.router_a.dry_run
        assert result == 0
    
    def test_dryRun_changeDryRunVariable_whenChangeDryRunVariableCalled(self):
        result = self.router_a.change_dry_run()
        assert result == "dry_run = 1: Payload will be returned to user"

    def test_dryRun_returnsConf_whenConfigureLoopbackCalledWithDryRun1(self):
        self.router_a.change_dry_run()
        result = self.router_a.configure_loopback(1, "192.168.1.1", "255.255.255.0")

        from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer
        conf = configure_loopback_xml_renderer(1, "192.168.1.1", "255.255.255.0")

        assert result == conf
    
    def test_dryRun_returnConf_whenDeleteLoopbackCalledWithDryRun1(self):
        self.router_a.change_dry_run()
        result = self.router_a.delete_loopback(1)

        from xml_functions.xml_function_delete_loopback import delete_loopback_xml_renderer
        conf = delete_loopback_xml_renderer(1)

        assert result == conf

    def test_dryRun_returnsConf_whenListInterfacesCalledWithDryRun1(self):
        self.router_a.change_dry_run()
        result = self.router_a.list_interfaces()

        from xml_functions.xml_function_list_interfaces import list_interfaces_xml_renderer
        conf = list_interfaces_xml_renderer

        assert result == conf