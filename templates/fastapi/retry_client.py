"""
Forge Protocol — HTTP Client with Retry Template (FastAPI)
Source: iiko-assistant (production patterns)

Async HTTP client with:
- Exponential backoff retry (tenacity)
- Token caching with expiry buffer
- Automatic token refresh on 401

Dependencies: pip install tenacity httpx

Usage:
  client = ExternalAPIClient(base_url="https://api.example.com", api_key="...")
  data = await client.get("/endpoint")
"""

import time
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class ExternalAPIClient:
    """Async HTTP client with retry and token management.

    Adapt _authenticate() and _headers() for your API's auth scheme.
    """

    def __init__(self, base_url: str, api_key: str = "", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._token: str | None = None
        self._token_expires_at: float = 0
        self._http = httpx.AsyncClient(timeout=timeout)

    async def _ensure_token(self) -> str:
        """Get a valid token, refreshing if expired or about to expire."""
        if self._token and time.time() < self._token_expires_at - 120:  # 2min buffer
            return self._token
        return await self._authenticate()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def _authenticate(self) -> str:
        """Fetch a new access token. Override for your API's auth endpoint."""
        resp = await self._http.post(
            f"{self.base_url}/auth/token",
            json={"apiKey": self.api_key},
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["token"]
        self._token_expires_at = time.time() + 3300  # 55 min (adjust per API)
        logger.info("api_token_refreshed", extra={"base_url": self.base_url})
        return self._token

    async def _headers(self) -> dict[str, str]:
        token = await self._ensure_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def get(self, endpoint: str, params: dict | None = None) -> dict:
        """GET with retry and auto token refresh on 401."""
        headers = await self._headers()
        resp = await self._http.get(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            headers=headers,
            params=params,
        )
        if resp.status_code == 401:
            await self._authenticate()
            headers = await self._headers()
            resp = await self._http.get(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                headers=headers,
                params=params,
            )
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def post(self, endpoint: str, payload: dict) -> dict:
        """POST with retry and auto token refresh on 401."""
        headers = await self._headers()
        resp = await self._http.post(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            json=payload,
            headers=headers,
        )
        if resp.status_code == 401:
            await self._authenticate()
            headers = await self._headers()
            resp = await self._http.post(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                json=payload,
                headers=headers,
            )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._http.aclose()
