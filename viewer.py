"""
Terminal Viewer for Bluesky data
Provides an interactive interface to view and manage users and posts
"""

import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box
from rich.text import Text
from database import Database
from models import User, Post
from atproto import Client


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
[yellow]3.[/yellow] Browse Top Posts from Bluesky
[yellow]4.[/yellow] Exit
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

    def browse_bluesky_posts(self) -> None:
        """Browse top posts from Bluesky and add them to the database"""
        self.console.print("[cyan]Fetching top posts from Bluesky...[/cyan]")

        try:
            client = Client()
            # Get posts from the "What's Hot" feed (popular posts)
            response = client.app.bsky.feed.get_timeline(limit=20)

            if not response.feed:
                self.console.print("[yellow]No posts found.[/yellow]")
                return

            # Display posts
            self.console.print(f"\n[bold green]Found {len(response.feed)} posts[/bold green]\n")

            for idx, feed_view in enumerate(response.feed, 1):
                post = feed_view.post
                author = post.author

                # Extract post data
                username = author.handle
                display_name = author.display_name or username
                post_text = post.record.text if hasattr(post.record, 'text') else ""
                post_uri = post.uri

                # Convert AT URI to web URL
                # Format: at://did:plc:xxx/app.bsky.feed.post/yyy
                parts = post_uri.split('/')
                if len(parts) >= 4:
                    post_id = parts[-1]
                    post_url = f"https://bsky.app/profile/{username}/post/{post_id}"
                else:
                    post_url = post_uri

                # Create a nice display box for each post
                post_info = Text()
                post_info.append(f"#{idx} ", style="bold yellow")
                post_info.append(f"{display_name}", style="bold cyan")
                post_info.append(f" (@{username})\n", style="cyan")
                post_info.append(f"{post_text[:200]}", style="white")
                if len(post_text) > 200:
                    post_info.append("...", style="dim")
                post_info.append(f"\n\n{post_url}", style="blue underline")

                self.console.print(Panel(post_info, border_style="green", padding=(1, 2)))

                # Ask if user wants to add this post
                add = Confirm.ask("Add this post to your database?", default=False)

                if add:
                    # Check if user exists, if not add them
                    if not self.db.get_user(username):
                        self.db.add_user(username, score=0)
                        self.console.print(f"[green]✓ Added user: {username}[/green]")

                    # Add the post
                    if self.db.add_post(post_url, username, score=0):
                        self.console.print(f"[green]✓ Post added to database![/green]")
                    else:
                        self.console.print(f"[yellow]Post already in database.[/yellow]")

                self.console.print()

                # Ask if they want to continue browsing
                if idx < len(response.feed):
                    continue_browsing = Confirm.ask("Continue browsing?", default=True)
                    if not continue_browsing:
                        break

            self.console.print("[bold cyan]Done browsing![/bold cyan]")

        except Exception as e:
            self.console.print(f"[red]Error fetching posts from Bluesky: {str(e)}[/red]")
            self.console.print("[yellow]Note: Bluesky browsing works without authentication for public posts.[/yellow]")

    def run(self) -> None:
        """Run the interactive viewer"""
        self.console.print("[bold cyan]Welcome to Bluesky Terminal Viewer![/bold cyan]\n")

        while True:
            try:
                self.show_menu()
                choice = Prompt.ask("Select an option", default="4")

                if choice == "1":
                    self.view_all_users()
                elif choice == "2":
                    self.view_all_posts()
                elif choice == "3":
                    self.browse_bluesky_posts()
                elif choice == "4":
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
