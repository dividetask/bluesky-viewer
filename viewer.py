"""
Terminal Viewer for Bluesky data
Provides an interactive interface to view and manage users and posts
"""

import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import box
from database import Database
from models import User, Post


class BlueskyViewer:
    """Interactive terminal viewer for Bluesky data"""

    def __init__(self, db_path: str = "bluesky_data.json"):
        self.db = Database(db_path)
        self.console = Console()

    def show_menu(self) -> None:
        """Display main menu"""
        menu_text = """
[bold cyan]Bluesky Terminal Viewer[/bold cyan]

[yellow]1.[/yellow] View All Users
[yellow]2.[/yellow] View All Posts
[yellow]3.[/yellow] View Top Users
[yellow]4.[/yellow] View Top Posts
[yellow]5.[/yellow] View Posts by User
[yellow]6.[/yellow] Add User
[yellow]7.[/yellow] Add Post
[yellow]8.[/yellow] Update User Score
[yellow]9.[/yellow] Update Post Score
[yellow]10.[/yellow] Delete User
[yellow]11.[/yellow] Delete Post
[yellow]12.[/yellow] Exit
"""
        self.console.print(Panel(menu_text, border_style="cyan"))

    def display_users(self, users: list, title: str = "Users") -> None:
        """Display users in a formatted table"""
        if not users:
            self.console.print("[yellow]No users found.[/yellow]")
            return

        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Username", style="cyan", no_wrap=True)
        table.add_column("Score", justify="right", style="green")

        for user in users:
            table.add_row(user["username"], str(user["score"]))

        self.console.print(table)

    def display_posts(self, posts: list, title: str = "Posts") -> None:
        """Display posts in a formatted table"""
        if not posts:
            self.console.print("[yellow]No posts found.[/yellow]")
            return

        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Link", style="cyan", overflow="fold")
        table.add_column("Username", style="yellow")
        table.add_column("Score", justify="right", style="green")

        for post in posts:
            table.add_row(post["link"], post["username"], str(post["score"]))

        self.console.print(table)

    def view_all_users(self) -> None:
        """View all users"""
        users = self.db.get_all_users()
        self.display_users(users, "All Users")

    def view_all_posts(self) -> None:
        """View all posts"""
        posts = self.db.get_all_posts()
        self.display_posts(posts, "All Posts")

    def view_top_users(self) -> None:
        """View top users by score"""
        limit = IntPrompt.ask("How many top users to display?", default=10)
        users = self.db.get_top_users(limit)
        self.display_users(users, f"Top {limit} Users")

    def view_top_posts(self) -> None:
        """View top posts by score"""
        limit = IntPrompt.ask("How many top posts to display?", default=10)
        posts = self.db.get_top_posts(limit)
        self.display_posts(posts, f"Top {limit} Posts")

    def view_posts_by_user(self) -> None:
        """View posts by a specific user"""
        username = Prompt.ask("Enter username")
        posts = self.db.get_posts_by_user(username)
        self.display_posts(posts, f"Posts by {username}")

    def add_user(self) -> None:
        """Add a new user"""
        username = Prompt.ask("Enter username")
        score = IntPrompt.ask("Enter initial score", default=0)

        if self.db.add_user(username, score):
            self.console.print(f"[green]✓ User '{username}' added successfully![/green]")
        else:
            self.console.print(f"[red]✗ User '{username}' already exists![/red]")

    def add_post(self) -> None:
        """Add a new post"""
        link = Prompt.ask("Enter post link")
        username = Prompt.ask("Enter username")
        score = IntPrompt.ask("Enter initial score", default=0)

        if self.db.add_post(link, username, score):
            self.console.print(f"[green]✓ Post added successfully![/green]")
        else:
            self.console.print(f"[red]✗ Post with this link already exists![/red]")

    def update_user_score(self) -> None:
        """Update a user's score"""
        username = Prompt.ask("Enter username")
        user = self.db.get_user(username)

        if not user:
            self.console.print(f"[red]✗ User '{username}' not found![/red]")
            return

        self.console.print(f"Current score: {user['score']}")
        new_score = IntPrompt.ask("Enter new score")

        if self.db.update_user_score(username, new_score):
            self.console.print(f"[green]✓ User score updated successfully![/green]")
        else:
            self.console.print(f"[red]✗ Failed to update user score![/red]")

    def update_post_score(self) -> None:
        """Update a post's score"""
        link = Prompt.ask("Enter post link")
        post = self.db.get_post_by_link(link)

        if not post:
            self.console.print(f"[red]✗ Post not found![/red]")
            return

        self.console.print(f"Current score: {post['score']}")
        new_score = IntPrompt.ask("Enter new score")

        if self.db.update_post_score(link, new_score):
            self.console.print(f"[green]✓ Post score updated successfully![/green]")
        else:
            self.console.print(f"[red]✗ Failed to update post score![/red]")

    def delete_user(self) -> None:
        """Delete a user"""
        username = Prompt.ask("Enter username to delete")
        confirm = Prompt.ask(f"Are you sure you want to delete '{username}'? (yes/no)", default="no")

        if confirm.lower() == "yes":
            if self.db.delete_user(username):
                self.console.print(f"[green]✓ User '{username}' deleted successfully![/green]")
            else:
                self.console.print(f"[red]✗ User '{username}' not found![/red]")
        else:
            self.console.print("[yellow]Deletion cancelled.[/yellow]")

    def delete_post(self) -> None:
        """Delete a post"""
        link = Prompt.ask("Enter post link to delete")
        confirm = Prompt.ask("Are you sure you want to delete this post? (yes/no)", default="no")

        if confirm.lower() == "yes":
            if self.db.delete_post(link):
                self.console.print(f"[green]✓ Post deleted successfully![/green]")
            else:
                self.console.print(f"[red]✗ Post not found![/red]")
        else:
            self.console.print("[yellow]Deletion cancelled.[/yellow]")

    def run(self) -> None:
        """Run the interactive viewer"""
        self.console.print("[bold cyan]Welcome to Bluesky Terminal Viewer![/bold cyan]\n")

        while True:
            try:
                self.show_menu()
                choice = Prompt.ask("Select an option", default="12")

                if choice == "1":
                    self.view_all_users()
                elif choice == "2":
                    self.view_all_posts()
                elif choice == "3":
                    self.view_top_users()
                elif choice == "4":
                    self.view_top_posts()
                elif choice == "5":
                    self.view_posts_by_user()
                elif choice == "6":
                    self.add_user()
                elif choice == "7":
                    self.add_post()
                elif choice == "8":
                    self.update_user_score()
                elif choice == "9":
                    self.update_post_score()
                elif choice == "10":
                    self.delete_user()
                elif choice == "11":
                    self.delete_post()
                elif choice == "12":
                    self.console.print("\n[bold cyan]Thank you for using Bluesky Terminal Viewer![/bold cyan]")
                    sys.exit(0)
                else:
                    self.console.print("[red]Invalid option. Please try again.[/red]")

                self.console.print()  # Empty line for spacing

            except KeyboardInterrupt:
                self.console.print("\n\n[bold cyan]Thank you for using Bluesky Terminal Viewer![/bold cyan]")
                sys.exit(0)
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    viewer = BlueskyViewer()
    viewer.run()
