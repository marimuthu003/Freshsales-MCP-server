import pytest
import json
from freshsales_mcp.tools.contacts import get_tools

@pytest.mark.asyncio
async def test_get_contact(mock_client):
    tools, _dispatch = get_tools(mock_client)
    
    mock_client.get.return_value = {"contact": {"id": 123, "first_name": "Test"}}
    
    result = await _dispatch("freshsales_get_contact", {"contact_id": 123})
    
    assert result["contact"]["first_name"] == "Test"
    mock_client.get.assert_called_once_with("/contacts/123", params={})

@pytest.mark.asyncio
async def test_create_contact(mock_client):
    tools, _dispatch = get_tools(mock_client)
    
    mock_client.post.return_value = {"contact": {"id": 456}}
    
    result = await _dispatch("freshsales_create_contact", {"first_name": "New"})
    
    assert result["contact"]["id"] == 456
    mock_client.post.assert_called_once_with("/contacts", body={"contact": {"first_name": "New"}})
