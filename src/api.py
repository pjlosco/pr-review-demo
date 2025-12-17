"""
Simple API shim for the hello-world demo.
"""

from src.auth import HelloService


class HelloAPI:
    """Minimal API that returns a two-line greeting."""
    
    def __init__(self):
        self.hello_service = HelloService()
    
    def get_greeting(self) -> dict:
        greeting = self.hello_service.get_greeting()
        return {
            "status": "success",
            "lines": greeting["lines"],
            "started_at": greeting["started_at"]
        }

