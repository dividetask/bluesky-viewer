"""
Data models for Bluesky Terminal Viewer
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a Bluesky user"""
    username: str
    score: int = 0

    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "username": self.username,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            username=data["username"],
            score=data.get("score", 0)
        )


@dataclass
class Post:
    """Represents a Bluesky post"""
    link: str
    username: str
    score: int = 0

    def to_dict(self) -> dict:
        """Convert post to dictionary"""
        return {
            "link": self.link,
            "username": self.username,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Post':
        """Create post from dictionary"""
        return cls(
            link=data["link"],
            username=data["username"],
            score=data.get("score", 0)
        )
