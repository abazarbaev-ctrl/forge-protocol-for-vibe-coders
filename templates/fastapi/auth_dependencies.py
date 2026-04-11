"""
Forge Protocol — Auth Dependencies Template (FastAPI)
Source: AIRIS (5/5 quality)

Composable dependency chain:
  get_user_id -> get_current_user -> require_active_subscription

Swap Firebase for any auth provider (Auth0, Cognito, Supabase).
The pattern stays the same — only verify_token() changes.

Usage:
  @router.get("/protected")
  async def endpoint(user=Depends(get_current_user)):
      ...

  @router.post("/premium")
  async def endpoint(user=Depends(require_active)):
      ...
"""

import logging
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


# --- ADAPT THIS SECTION TO YOUR AUTH PROVIDER ---

def verify_token(token: str) -> dict:
    """Verify auth token and return decoded claims.

    Replace this with your auth provider:
    - Firebase: firebase_admin.auth.verify_id_token(token)
    - Auth0: jwt.decode(token, ...) with JWKS
    - Supabase: supabase.auth.get_user(token)

    Must return dict with at minimum: {"uid": "user_id_string"}
    Must raise HTTPException(401) on failure.
    """
    # PLACEHOLDER — replace with real verification
    raise HTTPException(401, "Auth provider not configured")


# --- DEPENDENCY CHAIN (usually no changes needed) ---

async def get_user_id(
    cred: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Lightweight auth: verify token, return user ID. No DB call."""
    if not cred:
        raise HTTPException(401, "Authorization required")
    decoded = verify_token(cred.credentials)
    return decoded["uid"]


async def get_current_user(user_id: str = Depends(get_user_id)):
    """Full auth: verify token + look up user in database.

    Replace the DB query with your ORM/query pattern.
    """
    # PLACEHOLDER — replace with your DB lookup
    # user = await db.fetchrow("SELECT * FROM users WHERE auth_id = $1", user_id)
    # if not user:
    #     raise HTTPException(401, "User not found")
    # return dict(user)
    raise HTTPException(501, "get_current_user not implemented")


async def require_active(user=Depends(get_current_user)):
    """Full auth + subscription/status check.

    Returns user dict with subscription info attached.
    Raises 402 Payment Required if subscription expired.
    """
    # PLACEHOLDER — replace with your subscription check
    # sub = await db.fetchrow("SELECT * FROM subscriptions WHERE user_id = $1", user["id"])
    # if not sub or sub["status"] != "active":
    #     raise HTTPException(402, detail=json.dumps({
    #         "reason": "inactive", "message": "Subscription required"
    #     }))
    # user["subscription"] = dict(sub)
    return user
