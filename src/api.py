"""
API endpoints - BAD IMPLEMENTATION FOR TESTING
This intentionally violates acceptance criteria to trigger negative review.
"""

from typing import Optional
from src.auth import AuthService, AuthenticationError

# BAD: Global state
request_count = 0

class AuthAPI:
    def __init__(self):
        self.auth_service = AuthService()
        # BAD: No rate limiting
        # BAD: No request logging
    
    def handle_login(self, provider: str, auth_code: str) -> dict:
        """
        BAD: Returns 200 for all responses, no proper HTTP status codes
        BAD: No input validation
        BAD: No rate limiting
        BAD: Exposes internal errors to client
        """
        global request_count
        request_count += 1
        
        # BAD: No input validation
        # BAD: No rate limiting check
        
        try:
            session_token = self.auth_service.login(provider, auth_code)
            # BAD: Always returns 200, should return 201 for created resource
            # BAD: No HTTP status code in response
            return {
                "status": "success",
                "session_token": session_token,
                "message": "Login successful"
                # BAD: Missing HTTP status code
            }
        except AuthenticationError as e:
            # BAD: Returns 200 with error, should return 401
            # BAD: No HTTP status code
            return {
                "status": "error",
                "error": str(e)
                # BAD: Should return HTTP 401 Unauthorized
            }
        except Exception as e:
            # BAD: Exposes internal error details
            # BAD: Returns 200, should return 500
            # BAD: No HTTP status code
            return {
                "status": "error",
                "error": f"Internal error: {str(e)}"  # BAD: Exposing internal errors
            }
    
    def handle_logout(self, session_token: str) -> dict:
        """
        BAD: No proper HTTP status codes
        BAD: No input validation
        """
        # BAD: No input validation
        success = self.auth_service.logout(session_token)
        if success:
            # BAD: Should return 200, but no HTTP status code in response
            return {
                "status": "success",
                "message": "Logout successful"
            }
        else:
            # BAD: Returns 200 with error, should return 404
            # BAD: No HTTP status code
            return {
                "status": "error",
                "error": "Session not found"
                # BAD: Should return HTTP 404 Not Found
            }
    
    def handle_validate(self, session_token: str) -> dict:
        """
        BAD: No proper HTTP status codes
        BAD: No input validation
        """
        # BAD: No input validation
        user = self.auth_service.validate_session(session_token)
        if user:
            # BAD: No HTTP status code
            return {
                "status": "success",
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "name": user.name
                }
            }
        else:
            # BAD: Returns 200 with error, should return 401
            # BAD: No HTTP status code
            return {
                "status": "error",
                "error": "Invalid or expired session"
                # BAD: Should return HTTP 401 Unauthorized
            }
    
    def handle_sql_query(self, query: str) -> dict:
        """
        BAD: SQL injection vulnerability
        BAD: This method shouldn't exist in auth API
        """
        # BAD: CRITICAL SECURITY ISSUE - SQL injection vulnerability
        # BAD: No input validation
        # BAD: No parameterized queries
        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # BAD: Direct string interpolation - SQL injection risk
        cursor.execute(f"SELECT * FROM users WHERE email = '{query}'")
        results = cursor.fetchall()
        conn.close()
        return {"results": results}
