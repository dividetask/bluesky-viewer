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
        self.console.print("\n[bold cyan]Browse Posts from Bluesky[/bold cyan]\n")
        self.console.print("[cyan]Attempting to fetch posts...[/cyan]")

        client = Client()
        needs_auth = False

        # Try to browse without authentication first
        try:
            # Use a popular feed generator URI for discovering posts
            feed_uri = "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot"

            response = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 20})

            if response.feed:
                self.console.print("[green]✓ Connected successfully (no login required)![/green]\n")
            else:
                needs_auth = True

        except Exception as e:
            error_msg = str(e)
            # Check if error is authentication-related
            if "401" in error_msg or "403" in error_msg or "authentication" in error_msg.lower():
                needs_auth = True
            else:
                self.console.print(f"[red]Error: {error_msg}[/red]")
                self.console.print("[yellow]Could not connect to Bluesky. Please try again later.[/yellow]")
                return

        # If authentication is needed, prompt for login
        if needs_auth:
            self.console.print("\n[yellow]Bluesky API requires authentication.[/yellow]")
            self.console.print("[dim]Your credentials are only used for this session and are not stored.[/dim]\n")

            do_login = Confirm.ask("Login with your Bluesky account?", default=True)

            if not do_login:
                self.console.print("\n[yellow]Cannot browse without authentication.[/yellow]")
                self.console.print("[dim]You can create a free account at https://bsky.app[/dim]")
                return

            # Get login credentials
            handle = Prompt.ask("Enter your Bluesky handle (e.g., username.bsky.social)")
            password = Prompt.ask("Enter your password", password=True)

            self.console.print("\n[cyan]Logging in...[/cyan]")

            try:
                client = Client()
                client.login(handle, password)
                self.console.print("[green]✓ Logged in successfully![/green]\n")

                # Fetch posts after authentication
                self.console.print("[cyan]Fetching top posts...[/cyan]")
                response = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': 20})

            except Exception as e:
                error_msg = str(e)
                self.console.print(f"\n[red]Error: {error_msg}[/red]")

                if "401" in error_msg or "authentication" in error_msg.lower():
                    self.console.print("[yellow]Invalid credentials. Please check your handle and password.[/yellow]")
                else:
                    self.console.print("[yellow]Could not connect to Bluesky. Please try again later.[/yellow]")
                return

        # Display the posts
        if not response.feed:
            self.console.print("[yellow]No posts found.[/yellow]")
            return

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
