"""
JSON Database Manager for Bluesky Terminal Viewer
Handles persistence of users and posts data
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class Database:
    """Simple JSON-based database for storing users and posts"""

    def __init__(self, db_path: str = "bluesky_data.json"):
        self.db_path = db_path
        self.data = self._load()

    def _load(self) -> Dict:
        """Load database from JSON file"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._get_default_structure()
        return self._get_default_structure()

    def _get_default_structure(self) -> Dict:
        """Return the default database structure"""
        return {
            "users": [],
            "posts": []
        }

    def save(self) -> None:
        """Save database to JSON file"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # User operations
    def add_user(self, username: str, score: int = 0) -> bool:
        """Add a new user to the database"""
        if self.get_user(username):
            return False  # User already exists

        self.data["users"].append({
            "username": username,
            "score": score
        })
        self.save()
        return True

    def get_user(self, username: str) -> Optional[Dict]:
        """Get a user by username"""
        for user in self.data["users"]:
            if user["username"] == username:
                return user
        return None

    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        return self.data["users"]

    def update_user_score(self, username: str, score: int) -> bool:
        """Update a user's score"""
        user = self.get_user(username)
        if user:
            user["score"] = score
            self.save()
            return True
        return False

    def delete_user(self, username: str) -> bool:
        """Delete a user from the database"""
        for i, user in enumerate(self.data["users"]):
            if user["username"] == username:
                self.data["users"].pop(i)
                self.save()
                return True
        return False

    # Post operations
    def add_post(self, link: str, username: str, score: int = 0) -> bool:
        """Add a new post to the database"""
        if self.get_post_by_link(link):
            return False  # Post already exists

        self.data["posts"].append({
            "link": link,
            "username": username,
            "score": score
        })
        self.save()
        return True

    def get_post_by_link(self, link: str) -> Optional[Dict]:
        """Get a post by its link"""
        for post in self.data["posts"]:
            if post["link"] == link:
                return post
        return None

    def get_all_posts(self) -> List[Dict]:
        """Get all posts"""
        return self.data["posts"]

    def get_posts_by_user(self, username: str) -> List[Dict]:
        """Get all posts by a specific user"""
        return [post for post in self.data["posts"] if post["username"] == username]

    def update_post_score(self, link: str, score: int) -> bool:
        """Update a post's score"""
        post = self.get_post_by_link(link)
        if post:
            post["score"] = score
            self.save()
            return True
        return False

    def delete_post(self, link: str) -> bool:
        """Delete a post from the database"""
        for i, post in enumerate(self.data["posts"]):
            if post["link"] == link:
                self.data["posts"].pop(i)
                self.save()
                return True
        return False

    def get_top_users(self, limit: int = 10) -> List[Dict]:
        """Get top users by score"""
        sorted_users = sorted(self.data["users"], key=lambda x: x["score"], reverse=True)
        return sorted_users[:limit]

    def get_top_posts(self, limit: int = 10) -> List[Dict]:
        """Get top posts by score"""
        sorted_posts = sorted(self.data["posts"], key=lambda x: x["score"], reverse=True)
        return sorted_posts[:limit]
