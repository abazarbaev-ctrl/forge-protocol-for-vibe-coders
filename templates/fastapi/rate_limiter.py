"""
Forge Protocol — Rate Limiter Template (FastAPI)
Source: AIRIS (5/5 quality)

Per-user rate limiting using JWT user ID.
Falls back to IP address for unauthenticated requests.

Dependencies: pip install slowapi

Usage:
  from app.core.rate_limiter import limiter, setup_rate_limiter
  setup_rate_limiter(app)

  @router.post("/ai/endpoint")
  @limiter.limit("30/minute")
  async def endpoint(request: Request):
      ...
"""

import base64
import json

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from fastapi import FastAPI


def get_user_key(request: Request) -> str:
    """Extract user ID from Bearer token for per-user rate limiting.

    Decodes JWT payload without crypto verification (auth handles that).
    Falls back to client IP when token is missing or malformed.
    """
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            payload = token.split(".")[1]
            payload += "=" * (4 - len(payload) % 4)
            data = json.loads(base64.urlsafe_b64decode(payload))
            uid = data.get("user_id") or data.get("sub")
            if uid:
                return uid
        except Exception:
            pass
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_key)


def setup_rate_limiter(app: FastAPI):
    """Attach rate limiter to FastAPI app. Call once in main.py."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
