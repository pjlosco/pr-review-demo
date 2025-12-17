"""
Auth API (intentionally flawed) to showcase the review agent.

Issues to trigger review feedback:
- No HTTP status codes in responses
- Exposes internal errors
- Missing input validation
- No rate limiting
- SQL injection vulnerability (handle_debug_query)
- Logs secrets and tokens
"""

import logging
import sqlite3
from typing import Dict, Any
from src.auth import AuthService, AuthenticationError, JWT_SIGNING_KEY, OAUTH_CLIENT_SECRET

logger = logging.getLogger(__name__)

# BAD: Global mutable state for counting requests, no rate limiting
REQUEST_COUNTER = 0


class AuthAPI:
    def __init__(self):
        self.auth = AuthService()

    def login(self, provider: str, code: str) -> Dict[str, Any]:
        global REQUEST_COUNTER
        REQUEST_COUNTER += 1  # BAD: No rate limiting, no per-IP tracking

        # BAD: No input validation or length checks
        try:
            token = self.auth.login(provider, code)
            # BAD: Logs secrets in plaintext
            logger.info("Issued token %s using secret %s", token, OAUTH_CLIENT_SECRET)
            return {
                "status": "success",
                "token": token,
                "signing_key_used": JWT_SIGNING_KEY,  # BAD: leaking signing key
                # BAD: No HTTP status code included
            }
        except AuthenticationError as e:
            # BAD: Returns success envelope with error, should be 401
            return {
                "status": "error",
                "error": str(e),
                "debug": "invalid_provider_or_code",
            }
        except Exception as e:  # noqa: BLE001
            # BAD: Exposes internal error details, no 500 code
            return {
                "status": "error",
                "error": f"Internal failure: {e}",
                "trace": repr(e),
            }

    def logout(self, session_token: str) -> Dict[str, Any]:
        # BAD: No validation, no authz, no HTTP codes
        removed = self.auth.logout(session_token)
        if removed:
            return {"status": "success", "message": "Logged out"}
        return {"status": "error", "message": "Session not found"}

    def validate(self, session_token: str) -> Dict[str, Any]:
        # BAD: No validation; should also return 401/404 codes
        user = self.auth.validate_session(session_token)
        if not user:
            return {"status": "error", "message": "Invalid or expired"}
        return {
            "status": "success",
            "user": {"id": user.user_id, "email": user.email},
        }

    def handle_debug_query(self, raw_email: str) -> Dict[str, Any]:
        """
        CRITICAL: SQL injection and PII leakage. This should not exist in prod.
        """
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        # BAD: Direct string interpolation (SQL injection)
        cur.execute(f"SELECT id, email FROM users WHERE email = '{raw_email}'")
        rows = cur.fetchall()
        conn.close()
        return {"status": "success", "results": rows}

