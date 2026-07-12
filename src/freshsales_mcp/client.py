import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    pass


class FreshsalesClient:
    BASE = "https://{domain}.myfreshworks.com/crm/sales/api"

    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.base_url = self.BASE.format(domain=domain)
        self._http = httpx.AsyncClient(
            headers={
                "Authorization": f"Token token={api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(10.0),
            limits=httpx.Limits(max_connections=20),
        )

    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(min=1, max=4),
        retry=retry_if_exception_type(httpx.RequestError)
    )
    async def _request(self, method: str, path: str, request_kwargs: dict = None, **kwargs) -> dict:
        if request_kwargs is None:
            request_kwargs = kwargs
            
        r = await self._http.request(method, f"{self.base_url}{path}", **request_kwargs)

        remaining = r.headers.get("X-RateLimit-Remaining")
        if remaining and int(remaining) < 50:
            logger.warning(f"Freshsales rate limit low: {remaining} remaining")

        if r.status_code == 429:
            reset_at = r.headers.get("X-RateLimit-Reset", "unknown")
            raise RateLimitError(f"Rate limit hit. Resets at {reset_at}")

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                error_data = r.json()
            except Exception:
                raise e
            raise ValueError(f"Freshsales API Error ({r.status_code}): {error_data}") from e

        # Don't try to parse json for 204 No Content
        if r.status_code == 204:
            return {}
            
        return r.json()

    async def get(self, path: str, params: dict = None) -> dict:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, body: dict) -> dict:
        return await self._request("POST", path, json=body)

    async def post_multipart(self, path: str, files: dict, data: dict = None) -> dict:
        async with httpx.AsyncClient(
            headers={"Authorization": f"Token token={self.api_key}"}
        ) as client:
            r = await client.post(f"{self.base_url}{path}", files=files, data=data)
            r.raise_for_status()
            return r.json()

    async def put(self, path: str, body: dict) -> dict:
        return await self._request("PUT", path, json=body)

    async def delete(self, path: str) -> dict:
        return await self._request("DELETE", path)

    async def close(self):
        await self._http.aclose()
