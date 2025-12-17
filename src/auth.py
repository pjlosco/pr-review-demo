"""
Authentication module for demo purposes.

Intentionally contains issues to showcase the review agent:
- Hardcoded secrets
- Plaintext token storage
- No encryption or validation
- No rate limiting
- Predictable session tokens
"""

import os
import time
from typing import Optional, Dict
from datetime import datetime, timedelta

# BAD: Hardcoded secrets and tokens in code
OAUTH_CLIENT_SECRET = "hardcoded-demo-secret"  # CRITICAL: should be in secrets manager
JWT_SIGNING_KEY = "super-secret-signing-key"   # CRITICAL: plaintext key


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class User:
    """Represents a user in the system."""

    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.created_at = datetime.now()


class AuthService:
    """Service for handling user authentication."""

    def __init__(self):
        # BAD: Sessions stored in-memory, unencrypted, and never rotated
        self.sessions: Dict[str, Dict] = {}
        # BAD: Fixed 24h sessions; no configuration or short-lived tokens
        self.session_duration = timedelta(hours=24)
        # BAD: No rate limiting or login attempt tracking
        self.login_attempts: Dict[str, int] = {}

    def login(self, provider: str, auth_code: str) -> str:
        """
        Authenticate user with OAuth2 provider.

        Issues to flag:
        - No input validation or provider allowlist enforcement
        - Hardcoded secrets
        - No error handling for provider failures
        - Tokens stored plaintext in session
        """
        # BAD: No validation of provider casing/whitelist
        if provider not in ["google", "github"]:
            raise AuthenticationError(f"Unsupported provider: {provider}")

        # BAD: No validation of auth_code length/format
        if not auth_code:
            raise AuthenticationError("Authorization code required")

        # BAD: Exchange uses hardcoded secret, no timeout or retry
        access_token = self._exchange_code_for_token(provider, auth_code)

        # BAD: No try/except around provider call
        user_info = self._get_user_info(provider, access_token)

        # Create user
        user = User(
            user_id=user_info["id"],
            email=user_info["email"],
            name=user_info["name"],
        )

        # BAD: Predictable session token, no signing or hashing
        session_token = f"session_{int(time.time())}"

        # BAD: Store access token and user info in plaintext
        self.sessions[session_token] = {
            "user": user,
            "access_token": access_token,
            "expires_at": datetime.now() + self.session_duration,
            "created_at": datetime.now(),
        }

        return session_token

    def _exchange_code_for_token(self, provider: str, auth_code: str) -> str:
        # BAD: Fake token exchange, no HTTPS verification, no CSRF/state check
        return f"token_{provider}_{auth_code}_{OAUTH_CLIENT_SECRET}"

    def _get_user_info(self, provider: str, access_token: str) -> Dict:
        # BAD: Stubbed response, no verification of access_token
        return {
            "id": f"{provider}_user_123",
            "email": f"user@{provider}.com",
            "name": f"{provider.title()} User",
        }

    def _create_session(self, user: User) -> str:
        # UNUSED: Kept for compatibility; still predictable and insecure
        session_token = f"session_{int(time.time())}"
        expires_at = datetime.now() + self.session_duration
        self.sessions[session_token] = {
            "user": user,
            "expires_at": expires_at,
            "created_at": datetime.now(),
        }
        return session_token

    def validate_session(self, session_token: str) -> Optional[User]:
        # BAD: No logging, no audit trail
        if session_token not in self.sessions:
            return None

        session = self.sessions[session_token]

        # BAD: Timezone-naive comparison; no refresh token support
        if datetime.now() > session["expires_at"]:
            del self.sessions[session_token]
            return None

        return session["user"]

    def logout(self, session_token: str) -> bool:
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
