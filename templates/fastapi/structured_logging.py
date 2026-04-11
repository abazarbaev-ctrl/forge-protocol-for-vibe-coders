"""
Forge Protocol — Structured Logging Template (FastAPI/Python)
Source: AIRIS (5/5 quality)

JSON logging with request context propagation via ContextVars.
Cloud Run stdout -> Cloud Logging auto-parses JSON fields.
Works with any cloud provider that ingests JSON stdout.

Usage:
  from app.core.logging_config import setup_logging
  setup_logging()  # Call once in main.py
"""

import logging
import os
import uuid
from contextvars import ContextVar

from pythonjsonlogger import jsonlogger

# Context vars — set per-request in error_middleware.py
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")
user_id_var: ContextVar[str] = ContextVar("user_id", default="-")


class RequestContextFilter(logging.Filter):
    """Inject request_id and user_id into every log entry automatically."""
    def filter(self, record):
        record.request_id = request_id_var.get("-")
        record.user_id = user_id_var.get("-")
        record.tenant_id = os.environ.get("TENANT_ID", "default")
        return True


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def setup_logging():
    """Configure JSON structured logging. Call once at app startup."""
    handler = logging.StreamHandler()
    fmt = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "severity"},
    )
    handler.setFormatter(fmt)

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
    root.addFilter(RequestContextFilter())

    # Silence noisy libraries — add your own as needed
    for noisy in ["uvicorn.access", "httpx", "google", "firebase_admin"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)
