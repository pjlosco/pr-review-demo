"""
Authentication module - BAD IMPLEMENTATION FOR TESTING
This intentionally has many issues to trigger a negative review.
"""

import time
from typing import Optional, Dict
from datetime import datetime, timedelta

# BAD: Hardcoded credentials
ADMIN_PASSWORD = "admin123"
SECRET_KEY = "my-secret-key-12345"

class AuthenticationError(Exception):
    pass

class User:
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.created_at = datetime.now()

class AuthService:
    def __init__(self):
        # BAD: Storing sessions in memory without encryption
        self.sessions: Dict[str, Dict] = {}
        # BAD: Hardcoded session duration, not configurable
        self.session_duration = timedelta(hours=24)
        # BAD: No rate limiting
        self.login_attempts = {}
    
    def login(self, provider: str, auth_code: str) -> str:
        # BAD: No input validation
        # BAD: No rate limiting check
        # BAD: No error handling for network issues
        
        if provider not in ['google', 'github']:
            # BAD: No proper error handling, just raises
            raise AuthenticationError(f"Unsupported provider: {provider}")
        
        # BAD: No validation of auth_code
        if not auth_code:
            raise AuthenticationError("Code required")
        
        # BAD: Storing tokens in plain text
        access_token = f"token_{provider}_{auth_code}"
        
        # BAD: No error handling if provider API fails
        user_info = self._get_user_info(provider, access_token)
        
        # BAD: No validation of user_info
        user = User(
            user_id=user_info['id'],
            email=user_info['email'],
            name=user_info['name']
        )
        
        # BAD: Session token is predictable (timestamp-based)
        session_token = f"session_{int(time.time())}"
        
        # BAD: Storing session data without encryption
        # BAD: No expiration check before creating new session
        self.sessions[session_token] = {
            'user': user,
            'token': access_token,  # BAD: Storing access token in session
            'expires_at': datetime.now() + self.session_duration,
            'created_at': datetime.now()
        }
        
        return session_token
    
    def _get_user_info(self, provider: str, access_token: str) -> Dict:
        # BAD: No actual API call, just returns fake data
        # BAD: No error handling
        return {
            'id': f"{provider}_user_123",
            'email': f"user@{provider}.com",
            'name': f"{provider.title()} User"
        }
    
    def validate_session(self, session_token: str) -> Optional[User]:
        # BAD: No input validation
        # BAD: No logging of validation attempts
        
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # BAD: Time comparison without timezone handling
        if datetime.now() > session['expires_at']:
            del self.sessions[session_token]
            return None
        
        return session['user']
    
    def logout(self, session_token: str) -> bool:
        # BAD: No input validation
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
