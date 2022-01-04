from unittest import mock
import pytest

from sky_project import Router

@pytest.fixture
def router_a():
    router_a = Router()
    return router_a

def test_Router_createsRouterObject_whenRouterObjectInstantiated(router_a):
    result = isinstance(router_a, Router)
    assert result == True

def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouterA(router_a):
    with mock.patch("sky_project.manager") as mocked_manager: #at instance where sky_project.manager called, replaced with mock_manager
        router_a.configure_loopback("192.168.0.101", "830", "cisco", "cisco")
        result = mocked_manager.connect_ssh.assert_called_once_with(
            host='192.168.0.101',
            port='830',
            username='cisco',
            password='cisco',
            hostkey_verify=False,
            device_params={'name': 'csr'}) #asserts if mocked_manager.connect_ssh called with correct arguements
        assert result == None

def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalledRouterB():
    with mock.patch("sky_project.manager") as mocked_manager:
        router_b = Router()
        router_b.configure_loopback("192.168.0.102", "830", "router", "router")
        mocked_manager.connect_ssh.assert_called_once_with(
            host='192.168.0.102',
            port='830',
            username='router',
            password='router',
            hostkey_verify=False,
            device_params={'name': 'csr'})