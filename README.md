# Bluesky Terminal Viewer

A simple, interactive terminal-based viewer for discovering and tracking Bluesky posts and users with a local JSON database.

## Features

- **Browse Bluesky Posts**: Discover top posts directly from Bluesky's public feed
- **Local JSON Database**: Track interesting posts and users in a simple, human-readable JSON file
- **Interactive Terminal UI**: Beautiful, colorful interface powered by Rich library
- **Add Posts While Browsing**: Save posts and users to your database as you discover them
- **Persistent Storage**: All changes automatically saved to disk

## Database Structure

### Users Table
Each user entry contains:
- `username`: The user's Bluesky username
- `score`: A numeric score associated with the user

### Posts Table
Each post entry contains:
- `link`: URL link to the Bluesky post
- `username`: Username of the post author
- `score`: A numeric score associated with the post

## Requirements

- **Python 3.7 or higher** (NOT Python 2.x)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bluesky-viewer
```

2. Run the installation script:
```bash
./install.sh
```

This creates a virtual environment and installs all dependencies automatically.

## Usage

### Basic Usage

Run the viewer:
```bash
./run.sh
```

The script automatically uses the virtual environment, so you don't need to activate it manually.

**Alternative:** If you prefer to manage the virtual environment yourself:
```bash
source venv/bin/activate
python3 main.py
deactivate  # when done
```

### Custom Database Path

Specify a custom database file:
```bash
./run.sh --db /path/to/custom_database.json
```

### Interactive Menu

Once running, you'll see an interactive menu with the following options:

1. **View All Users** - Display all tracked users in a table
2. **View All Posts** - Display all saved posts in a table
3. **Browse Top Posts from Bluesky** - Discover new posts from Bluesky's public feed
4. **Exit** - Quit the application

## Example Workflow

```bash
# Start the viewer
./run.sh

# Select option 3 to browse posts from Bluesky
# The viewer will fetch top posts and display them one by one
# You'll see the author, post content, and URL for each post
# Choose whether to add interesting posts to your database

# Select option 1 to view all saved users
# Select option 2 to view all saved posts
```

### Browsing Bluesky Posts

When you select option 3, the viewer will:
1. Attempt to browse posts without requiring login
2. If authentication is needed, prompt you to login with your Bluesky handle and password
3. Fetch up to 20 popular posts from Bluesky's "What's Hot" feed
4. Display each post with author info and content
5. Ask if you want to add the post to your database
6. Automatically add the author if they're not already tracked
7. Continue to the next post or stop browsing

**Note:** The Bluesky API may require authentication. If you need to login, your credentials are only used for the session and are not stored. Don't have an account? Create a free one at https://bsky.app

## Database File Format

The JSON database file (`bluesky_data.json` by default) has the following structure:

```json
{
  "users": [
    {
      "username": "alice.bsky.social",
      "score": 100
    }
  ],
  "posts": [
    {
      "link": "https://bsky.app/profile/alice.bsky.social/post/123",
      "username": "alice.bsky.social",
      "score": 50
    }
  ]
}
```

## Project Structure

```
bluesky-viewer/
├── main.py           # Entry point for the application
├── viewer.py         # Terminal UI and interactive menu
├── database.py       # JSON database management
├── models.py         # Data models for User and Post
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Dependencies

- **rich** (>= 13.7.0): Terminal formatting and UI components
- **python-dateutil** (>= 2.8.2): Date handling utilities
- **atproto** (>= 0.0.55): Bluesky API client library


## Development

The codebase is organized into clear modules:

- `database.py`: Handles all database operations (CRUD for users and posts)
- `models.py`: Defines data structures for User and Post
- `viewer.py`: Implements the terminal UI, interactive menu, and Bluesky API integration
- `main.py`: Entry point with command-line argument parsing

### How It Works

The Bluesky browsing feature uses the AT Protocol (atproto) library to fetch posts from Bluesky's "What's Hot" feed. The viewer first attempts to browse without authentication. If the API requires login, you'll be prompted to enter your credentials, which are only used during the session and are never stored. When you add a post, both the post and the author are automatically saved to your local database for future reference.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
