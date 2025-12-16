"""
API endpoints for authentication.

This module provides REST API endpoints for user authentication.
All endpoints require proper error handling and return appropriate HTTP status codes.
"""

from typing import Optional
from src.auth import AuthService, AuthenticationError


class AuthAPI:
    """REST API handler for authentication endpoints."""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def handle_login(self, provider: str, auth_code: str) -> dict:
        """
        Handle POST /api/v1/auth/login request.
        
        Args:
            provider: OAuth2 provider ('google' or 'github')
            auth_code: Authorization code from OAuth2 callback
            
        Returns:
            Response dictionary with session token
        """
        try:
            session_token = self.auth_service.login(provider, auth_code)
            return {
                "status": "success",
                "session_token": session_token,
                "message": "Login successful"
            }
        except AuthenticationError as e:
            # Should return 401 status code
            return {
                "status": "error",
                "error": str(e)
            }
        except Exception as e:
            # Should return 500 status code
            return {
                "status": "error",
                "error": "Internal server error"
            }
    
    def handle_logout(self, session_token: str) -> dict:
        """
        Handle POST /api/v1/auth/logout request.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            Response dictionary
        """
        success = self.auth_service.logout(session_token)
        if success:
            return {
                "status": "success",
                "message": "Logout successful"
            }
        else:
            # Should return 404 if session not found
            return {
                "status": "error",
                "error": "Session not found"
            }
    
    def handle_validate(self, session_token: str) -> dict:
        """
        Handle GET /api/v1/auth/validate request.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Response dictionary with user info if valid
        """
        user = self.auth_service.validate_session(session_token)
        if user:
            return {
                "status": "success",
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "name": user.name
                }
            }
        else:
            # Should return 401 if session invalid
            return {
                "status": "error",
                "error": "Invalid or expired session"
            }

