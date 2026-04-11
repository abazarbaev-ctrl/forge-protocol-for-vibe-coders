"""
Forge Protocol — Health Check Endpoint Template (FastAPI)
Source: AIRIS (5/5 quality)

Reports service status, database connectivity, and dependency health.
Used by load balancers and monitoring to determine if the service is healthy.

Usage:
  from app.core.health import health_router
  app.include_router(health_router)
"""

import logging
import os
from fastapi import APIRouter

logger = logging.getLogger(__name__)

health_router = APIRouter()


@health_router.get("/health")
async def health():
    """Health check with dependency status.

    Adapt the checks below to your project's dependencies:
    - Database connection
    - Redis connection
    - External API availability
    """
    result = {
        "status": "ok",
        "service": os.environ.get("SERVICE_NAME", "api"),
        "tenant": os.environ.get("TENANT_ID", "default"),
    }

    # --- DATABASE CHECK (adapt to your ORM) ---
    # try:
    #     # asyncpg pool example:
    #     if db.pool is None:
    #         logger.info("health_check_db_reconnect")
    #         await db.connect()
    #     result["db_connected"] = db.pool is not None
    #
    #     # SQLAlchemy example:
    #     # async with async_session() as session:
    #     #     await session.execute(text("SELECT 1"))
    #     # result["db_connected"] = True
    # except Exception as e:
    #     result["db_connected"] = False
    #     logger.warning("health_check_db_failed", extra={"error": str(e)[:200]})

    # --- REDIS CHECK ---
    # try:
    #     await redis.ping()
    #     result["redis_connected"] = True
    # except Exception:
    #     result["redis_connected"] = False

    # Set overall status based on critical dependencies
    # if not result.get("db_connected", True):
    #     result["status"] = "degraded"

    return result
