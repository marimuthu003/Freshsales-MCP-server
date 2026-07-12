import pytest
import httpx
import respx
from freshsales_mcp.client import FreshsalesClient, RateLimitError

@pytest.fixture
def client():
    return FreshsalesClient(api_key="test_key", domain="test")

@pytest.mark.asyncio
@respx.mock
async def test_get_success(client):
    respx.get("https://test.myfreshworks.com/crm/sales/api/contacts").mock(return_value=httpx.Response(200, json={"contacts": []}))
    
    result = await client.get("/contacts")
    assert result == {"contacts": []}

@pytest.mark.asyncio
@respx.mock
async def test_error_parsing(client):
    error_payload = {"errors": {"email": ["cannot be blank"]}}
    respx.post("https://test.myfreshworks.com/crm/sales/api/contacts").mock(return_value=httpx.Response(400, json=error_payload))
    
    with pytest.raises(ValueError) as excinfo:
        await client.post("/contacts", body={})
    
    assert "Freshsales API Error (400)" in str(excinfo.value)
    assert "cannot be blank" in str(excinfo.value)

@pytest.mark.asyncio
@respx.mock
async def test_rate_limit(client):
    headers = {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "12345"}
    respx.get("https://test.myfreshworks.com/crm/sales/api/contacts").mock(return_value=httpx.Response(429, headers=headers))
    
    with pytest.raises(RateLimitError) as excinfo:
        await client.get("/contacts")
    
    assert "Resets at 12345" in str(excinfo.value)

@pytest.mark.asyncio
@respx.mock
async def test_post_multipart(client):
    respx.post("https://test.myfreshworks.com/crm/sales/api/files").mock(return_value=httpx.Response(200, json={"success": True}))
    
    files = {"file": ("test.txt", b"hello world")}
    result = await client.post_multipart("/files", files=files)
    assert result == {"success": True}
