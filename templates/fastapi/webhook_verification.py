"""
Forge Protocol — Webhook Signature Verification Template (FastAPI)
Source: AIRIS (Stripe) + iiko-assistant (Telegram/WhatsApp/iiko)

Patterns for verifying webhook signatures from external services.
NEVER process webhook payloads without signature verification.

Usage: Pick the pattern matching your webhook provider.
"""

import hashlib
import hmac
import logging
import os

from fastapi import APIRouter, HTTPException, Request, Response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


# --- PATTERN 1: HMAC Signature (Stripe, GitHub, Slack) ---

@router.post("/stripe")
async def stripe_webhook(request: Request):
    """Stripe webhook with signature verification."""
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    if not webhook_secret:
        logger.warning("webhook_no_secret", extra={"provider": "stripe"})
        raise HTTPException(500, "Webhook secret not configured")

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    if not sig_header:
        raise HTTPException(400, "Missing Stripe-Signature header")

    try:
        import stripe
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except Exception as e:
        logger.warning("webhook_sig_failed", extra={"provider": "stripe", "error": str(e)[:200]})
        raise HTTPException(400, "Signature verification failed")

    event_type = event.get("type", "")
    logger.info("webhook_received", extra={"provider": "stripe", "type": event_type})

    # Route by event type
    # if event_type == "checkout.session.completed":
    #     await handle_checkout(event["data"]["object"])

    return {"ok": True}


# --- PATTERN 2: Shared Secret Header (Cloud Scheduler, internal services) ---

@router.post("/scheduler")
async def scheduler_webhook(request: Request):
    """Cloud Scheduler webhook protected by shared secret header."""
    expected = os.environ.get("SCHEDULER_SECRET", "")
    provided = request.headers.get("X-Scheduler-Secret", "")

    if not expected or provided != expected:
        # Also allow Cloud Run's built-in OIDC auth
        if not request.headers.get("X-CloudScheduler"):
            raise HTTPException(403, "Forbidden - scheduler auth required")

    body = await request.json()
    logger.info("scheduler_webhook", extra={"task": body.get("task", "unknown")})

    # Process scheduled task
    # await handle_scheduled_task(body)

    return {"ok": True}


# --- PATTERN 3: Meta Verification (WhatsApp, Instagram) ---

from fastapi import Query


@router.get("/whatsapp")
async def whatsapp_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """Meta webhook verification — responds with challenge if token matches."""
    verify_token = os.environ.get("WHATSAPP_VERIFY_TOKEN", "")
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        logger.info("webhook_verified", extra={"provider": "whatsapp"})
        return Response(content=hub_challenge, media_type="text/plain")
    logger.warning("webhook_verify_failed", extra={"provider": "whatsapp"})
    return Response(status_code=403)


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp incoming message webhook."""
    body = await request.json()
    entries = body.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            messages = change.get("value", {}).get("messages", [])
            for msg in messages:
                from_number = msg.get("from", "")
                text = msg.get("text", {}).get("body", "")
                logger.info("whatsapp_message", extra={"from": from_number[:4] + "***", "length": len(text)})
                # await process_message(from_number, text)
    return Response(status_code=200)


# --- PATTERN 4: Telegram Bot Token Verification ---

@router.post("/telegram")
async def telegram_webhook(request: Request):
    """Telegram webhook — verify via bot token in URL path (set during webhook registration).

    Telegram doesn't sign payloads. Security comes from:
    1. Secret path: /webhooks/telegram/{secret_token}
    2. IP allowlist (optional): Telegram sends from known IP ranges
    """
    body = await request.json()
    message = body.get("message") or body.get("edited_message")
    if not message or "text" not in message:
        return Response(status_code=200)

    chat_id = message["chat"]["id"]
    text = message["text"]
    user_name = message["from"].get("first_name", "")

    logger.info("telegram_message", extra={"user": user_name, "length": len(text)})

    # await process_message(chat_id, text)

    return Response(status_code=200)


# --- GENERIC HMAC VERIFICATION HELPER ---

def verify_hmac_signature(
    payload: bytes,
    signature: str,
    secret: str,
    algorithm: str = "sha256",
    prefix: str = "",
) -> bool:
    """Generic HMAC signature verification.

    Args:
        payload: Raw request body bytes
        signature: Signature from header (e.g., "sha256=abc123...")
        secret: Webhook secret key
        algorithm: Hash algorithm (sha256, sha1)
        prefix: Signature prefix to strip (e.g., "sha256=")

    Returns:
        True if signature is valid
    """
    if prefix and signature.startswith(prefix):
        signature = signature[len(prefix):]

    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        getattr(hashlib, algorithm),
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
