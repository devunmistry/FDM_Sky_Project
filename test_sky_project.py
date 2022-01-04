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

def test_configureLoopback_callsNcclientManagerConnectssh_whenConfigureLoopbackCalled(router_a):
    with mock.patch("sky_project.manager") as mocked_manager: #at instance where manager called, replaced with mock_manager
        router_a.configure_loopback()
        result = mocked_manager.connect_ssh.assert_called_once_with(
            host='192.168.0.101',
            port='830', username='cisco',
            password='cisco',
            hostkey_verify=False,
            device_params={'name': 'csr'}) #asserts if mocked_manager.connect_ssh called with correct arguements
        assert result == None