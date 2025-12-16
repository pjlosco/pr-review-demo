"""
Authentication module for user login and session management.

This module implements OAuth2 authentication with Google and GitHub providers.
Sessions are maintained for 24 hours as per requirements.
"""

import time
from typing import Optional, Dict
from datetime import datetime, timedelta


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


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
        self.sessions: Dict[str, Dict] = {}
        self.session_duration = timedelta(hours=24)
    
    def login(self, provider: str, auth_code: str) -> str:
        """
        Authenticate user with OAuth2 provider.
        
        Args:
            provider: OAuth2 provider name ('google' or 'github')
            auth_code: Authorization code from OAuth2 callback
            
        Returns:
            Session token string
            
        Raises:
            AuthenticationError: If authentication fails
        """
        if provider not in ['google', 'github']:
            raise AuthenticationError(f"Unsupported provider: {provider}")
        
        # Exchange auth code for access token (simplified for demo)
        access_token = self._exchange_code_for_token(provider, auth_code)
        
        # Get user info from provider
        user_info = self._get_user_info(provider, access_token)
        
        # Create user
        user = User(
            user_id=user_info['id'],
            email=user_info['email'],
            name=user_info['name']
        )
        
        # Create session
        session_token = self._create_session(user)
        
        return session_token
    
    def _exchange_code_for_token(self, provider: str, auth_code: str) -> str:
        """Exchange authorization code for access token."""
        # Simplified implementation for demo
        return f"token_{provider}_{auth_code}"
    
    def _get_user_info(self, provider: str, access_token: str) -> Dict:
        """Get user information from provider."""
        # Simplified implementation for demo
        return {
            'id': f"{provider}_user_123",
            'email': f"user@{provider}.com",
            'name': f"{provider.title()} User"
        }
    
    def _create_session(self, user: User) -> str:
        """Create a new session for the user."""
        session_token = f"session_{int(time.time())}"
        expires_at = datetime.now() + self.session_duration
        
        self.sessions[session_token] = {
            'user': user,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
        
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[User]:
        """
        Validate a session token and return the user if valid.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            User object if session is valid, None otherwise
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        if datetime.now() > session['expires_at']:
            # Session expired
            del self.sessions[session_token]
            return None
        
        return session['user']
    
    def logout(self, session_token: str) -> bool:
        """
        Logout user by invalidating their session.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if logout successful, False if session not found
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False

