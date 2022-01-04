import pytest
from sky_project import Router

def test_Router_createsRouterObject_whenRouterObjectInstantiated():
    router = Router()
    result = isinstance(router, Router)
    assert result == True