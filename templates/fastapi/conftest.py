"""
Forge Protocol — Pytest Fixtures Template (FastAPI)
Source: AIRIS (5/5 quality)

Features:
- Session-scoped authenticated httpx client
- Configurable base URL (local/staging/prod)
- Token caching to prevent connection exhaustion
- Auto-marker injection for test parallelization
- Shared TestState for lifecycle tests

Usage:
  def test_endpoint(auth_client):
      r = auth_client.get("/api/resource")
      assert r.status_code == 200
"""

import os
import pytest
import httpx

# --- CONFIGURATION ---

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

# Test file classification for parallel execution
# "api" files call AI/slow endpoints — run sequentially
# "ordered" files have lifecycle dependencies — run sequentially
# Everything else is "fast" — safe for pytest-xdist -n 4
_API_TEST_FILES = frozenset({
    # Add filenames that call AI or rate-limited endpoints:
    # "test_ai.py",
    # "test_adversarial.py",
})

_ORDERED_TEST_FILES = frozenset({
    # Add filenames with create->get->update->delete dependencies:
    # "test_patients.py",
    # "test_episodes.py",
})


def pytest_collection_modifyitems(items):
    """Auto-apply markers based on filename."""
    for item in items:
        filename = item.fspath.basename
        if filename in _API_TEST_FILES:
            item.add_marker(pytest.mark.api)
        elif filename in _ORDERED_TEST_FILES:
            item.add_marker(pytest.mark.ordered)
        else:
            item.add_marker(pytest.mark.fast)


# --- TOKEN GENERATION (adapt to your auth provider) ---

_token_cache = {}


def generate_auth_token(user_id: str) -> str:
    """Generate an auth token for testing.

    Replace with your auth provider:
    - Firebase: firebase_admin.auth.create_custom_token(user_id) -> exchange
    - Auth0: auth0.get_token(...)
    - Simple: create JWT with test secret
    """
    if user_id in _token_cache:
        return _token_cache[user_id]

    # PLACEHOLDER — replace with real token generation
    token = f"test-token-{user_id}"
    _token_cache[user_id] = token
    return token


# --- SESSION-SCOPED FIXTURES ---

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token():
    """Generate an auth token once per session."""
    return generate_auth_token("test_user_99999")


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="session")
def client(base_url):
    """Shared httpx client for the test session."""
    with httpx.Client(base_url=base_url, timeout=httpx.Timeout(30, connect=10)) as c:
        yield c


@pytest.fixture(scope="session")
def auth_client(base_url, auth_headers):
    """Authenticated httpx client. Extended timeout for AI endpoints."""
    with httpx.Client(
        base_url=base_url,
        timeout=httpx.Timeout(90, connect=10, read=90, write=30),
        headers=auth_headers,
    ) as c:
        yield c


# --- SHARED STATE ---

class TestState:
    """Mutable state shared across ordered/lifecycle tests."""
    # Add fields for your domain:
    # resource_id: str = None
    # session_token: str = None
    pass


@pytest.fixture(scope="session")
def state():
    return TestState()
