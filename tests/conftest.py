import pytest
from unittest.mock import AsyncMock
from mcp.server import Server
from freshsales_mcp.client import FreshsalesClient

@pytest.fixture
def mock_client():
    client = FreshsalesClient(api_key="test", domain="test")
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.delete = AsyncMock()
    return client

@pytest.fixture
def server():
    return Server("test-server")
