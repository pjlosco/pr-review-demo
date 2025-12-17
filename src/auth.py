"""
Simple hello-world service for the demo branch.
"""
from typing import Dict, List
from datetime import datetime


class HelloService:
    """Minimal demo service that returns a two-line greeting."""
    
    def __init__(self):
        self.started_at = datetime.now()
    
    def get_greeting(self) -> Dict[str, List[str]]:
        return {
            "lines": [
                "Hello, world!",
                "Thanks for trying the PR Review demo."
            ],
            "started_at": self.started_at.isoformat()
        }

