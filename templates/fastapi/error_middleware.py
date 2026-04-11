"""
Forge Protocol — FastAPI Error Middleware Template
Source: AIRIS (5/5 quality)

Three-layer error handling:
1. Request context middleware (request_id, timing, user extraction)
2. Null byte security check (path traversal prevention)
3. Global exception handler (error classification: 400 vs 500)

Usage:
  from app.core.error_middleware import setup_error_handling
  setup_error_handling(app)
"""

import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import logging

logger = logging.getLogger(__name__)

# Context vars for request tracing (propagate into all log entries)
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")
user_id_var: ContextVar[str] = ContextVar("user_id", default="-")


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def setup_error_handling(app: FastAPI):
    """Attach all error-handling middleware to a FastAPI app."""

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        """Layer 1: Inject request_id, extract user from token, log timing."""
        rid = new_request_id()
        request_id_var.set(rid)

        # Lightweight user extraction from JWT (no verification — auth handles that)
        auth = request.headers.get("authorization", "")
        if auth.startswith("Bearer ") and len(auth) > 20:
            try:
                import base64
                import json
                parts = auth[7:].split(".")
                if len(parts) >= 2:
                    pad = parts[1] + "=" * (4 - len(parts[1]) % 4)
                    payload = json.loads(base64.urlsafe_b64decode(pad))
                    user_id_var.set(payload.get("sub", "-")[:20])
            except Exception:
                pass

        start = time.time()
        path = request.url.path
        method = request.method
        logger.info("request_start", extra={"method": method, "path": path})

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = int((time.time() - start) * 1000)
            logger.error(
                "request_error",
                extra={"method": method, "path": path, "duration_ms": duration_ms, "error": str(exc)[:200]},
                exc_info=True,
            )
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

        duration_ms = int((time.time() - start) * 1000)
        response.headers["X-Request-ID"] = rid

        # Only log slow requests (>5s) and errors to reduce noise
        if duration_ms > 5000 or response.status_code >= 400:
            logger.info(
                "request_end",
                extra={"method": method, "path": path, "status": response.status_code, "duration_ms": duration_ms},
            )
        return response

    @app.middleware("http")
    async def sanitize_null_bytes(request: Request, call_next):
        """Layer 2: Reject requests with null bytes — prevents path traversal attacks."""
        if "\x00" in str(request.url) or "%00" in str(request.url):
            return JSONResponse(status_code=400, content={"detail": "Invalid request: null bytes not allowed"})
        return await call_next(request)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Layer 3: Classify errors — input validation (400) vs server errors (500)."""
        err_str = str(exc)[:300]

        # Input validation errors -> 400 (not 500)
        validation_keywords = [
            "null byte", "invalid byte", "surrogate", "\\x00", "nul",
            "invalid input syntax", "value too long", "string data",
            "encoding", "codec", "character", "unicode", "surrogates not allowed",
        ]
        if any(kw in err_str.lower() for kw in validation_keywords):
            logger.warning("input_validation_error", extra={"path": str(request.url), "error": err_str})
            return JSONResponse(status_code=400, content={"detail": "Invalid input: contains invalid characters"})

        logger.error("unhandled_exception", extra={"path": str(request.url), "error": err_str}, exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
