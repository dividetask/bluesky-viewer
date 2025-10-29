#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the Bluesky database
"""

from database import Database
from models import User, Post


def main():
    # Initialize database
    db = Database("example_data.json")

    print("Bluesky Terminal Viewer - Example Usage\n")

    # Add some example users
    print("Adding users...")
    db.add_user("alice.bsky.social", 150)
    db.add_user("bob.bsky.social", 200)
    db.add_user("charlie.bsky.social", 75)
    print("✓ Users added\n")

    # Add some example posts
    print("Adding posts...")
    db.add_post("https://bsky.app/profile/alice.bsky.social/post/1", "alice.bsky.social", 50)
    db.add_post("https://bsky.app/profile/alice.bsky.social/post/2", "alice.bsky.social", 100)
    db.add_post("https://bsky.app/profile/bob.bsky.social/post/1", "bob.bsky.social", 75)
    db.add_post("https://bsky.app/profile/charlie.bsky.social/post/1", "charlie.bsky.social", 25)
    print("✓ Posts added\n")

    # View all users
    print("All users:")
    for user in db.get_all_users():
        print(f"  - {user['username']}: {user['score']} points")
    print()

    # View top users
    print("Top 2 users:")
    for user in db.get_top_users(2):
        print(f"  - {user['username']}: {user['score']} points")
    print()

    # View all posts
    print("All posts:")
    for post in db.get_all_posts():
        print(f"  - {post['link']}")
        print(f"    By: {post['username']}, Score: {post['score']}")
    print()

    # View posts by specific user
    print("Posts by alice.bsky.social:")
    for post in db.get_posts_by_user("alice.bsky.social"):
        print(f"  - {post['link']} (Score: {post['score']})")
    print()

    # Update scores
    print("Updating scores...")
    db.update_user_score("alice.bsky.social", 250)
    db.update_post_score("https://bsky.app/profile/bob.bsky.social/post/1", 150)
    print("✓ Scores updated\n")

    # View updated data
    print("Updated user (alice):")
    user = db.get_user("alice.bsky.social")
    print(f"  - {user['username']}: {user['score']} points")
    print()

    print("Updated post:")
    post = db.get_post_by_link("https://bsky.app/profile/bob.bsky.social/post/1")
    print(f"  - {post['link']}")
    print(f"    Score: {post['score']}")
    print()

    print(f"Data saved to: example_data.json")
    print("\nRun 'python main.py --db example_data.json' to view this data interactively!")


if __name__ == "__main__":
    main()
