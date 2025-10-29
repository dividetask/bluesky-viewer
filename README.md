# Bluesky Terminal Viewer

A simple, interactive terminal-based viewer for managing Bluesky users and posts with a local JSON database.

## Features

- **Local JSON Database**: All data stored in a simple, human-readable JSON file
- **User Management**: Add, view, update, and delete users with associated scores
- **Post Management**: Add, view, update, and delete posts with links and scores
- **Interactive Terminal UI**: Beautiful, colorful interface powered by Rich library
- **Sorting & Filtering**: View top users and posts by score, filter posts by user
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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bluesky-viewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the viewer with default settings:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

### Custom Database Path

Specify a custom database file:
```bash
python main.py --db /path/to/custom_database.json
```

### Interactive Menu

Once running, you'll see an interactive menu with the following options:

1. **View All Users** - Display all users in a table
2. **View All Posts** - Display all posts in a table
3. **View Top Users** - Display top N users by score
4. **View Top Posts** - Display top N posts by score
5. **View Posts by User** - Filter posts by a specific username
6. **Add User** - Add a new user with username and score
7. **Add Post** - Add a new post with link, username, and score
8. **Update User Score** - Modify a user's score
9. **Update Post Score** - Modify a post's score
10. **Delete User** - Remove a user from the database
11. **Delete Post** - Remove a post from the database
12. **Exit** - Quit the application

## Example Workflow

```bash
# Start the viewer
python main.py

# Select option 6 to add a user
# Enter username: alice.bsky.social
# Enter score: 100

# Select option 7 to add a post
# Enter link: https://bsky.app/profile/alice.bsky.social/post/123
# Enter username: alice.bsky.social
# Enter score: 50

# Select option 1 to view all users
# Select option 2 to view all posts
```

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

## Requirements

- Python 3.7 or higher

## Development

The codebase is organized into clear modules:

- `database.py`: Handles all database operations (CRUD for users and posts)
- `models.py`: Defines data structures for User and Post
- `viewer.py`: Implements the terminal UI and interactive functionality
- `main.py`: Entry point with command-line argument parsing

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
