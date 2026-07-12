import pytest
import json
from freshsales_mcp.tools.deals import get_tools

class MockServer:
    def __init__(self):
        self.call_tool_handler = None

    def list_tools(self):
        def decorator(f):
            return f
        return decorator

    def call_tool(self):
        def decorator(f):
            self.call_tool_handler = f
            return f
        return decorator

@pytest.mark.asyncio
async def test_create_deal(mock_client):
    server = MockServer()
    tools, _dispatch = get_tools(mock_client)
    
    mock_client.post.return_value = {"deal": {"id": 999, "name": "Big Deal"}}
    
    result = await _dispatch("freshsales_create_deal", {"name": "Big Deal", "amount": 1000})
    assert result == {"deal": {"id": 999, "name": "Big Deal"}}
    mock_client.post.assert_called_once_with("/deals", body={"deal": {"name": "Big Deal", "amount": 1000}})
