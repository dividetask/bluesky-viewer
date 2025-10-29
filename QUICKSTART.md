# Quick Start Guide

## Prerequisites

**Python 3.7 or higher required** - This will NOT work with Python 2.x

Check your Python version:
```bash
python3 --version
```

## Installation

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

   Or if pip is already Python 3:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the example script** to see it in action:
   ```bash
   python3 example.py
   ```

3. **Start the interactive viewer:**
   ```bash
   python3 main.py
   ```

   Or use the example data:
   ```bash
   python3 main.py --db example_data.json
   ```

**Alternative:** Make the script executable:
```bash
chmod +x main.py
./main.py
```

## First Steps

Once the viewer is running, try these options:

1. **Option 1** - View all users
2. **Option 2** - View all posts
3. **Option 6** - Add a new user
4. **Option 7** - Add a new post

## Example Usage

Add a user:
- Choose option 6
- Enter username: `john.bsky.social`
- Enter score: `100`

Add a post:
- Choose option 7
- Enter link: `https://bsky.app/profile/john.bsky.social/post/abc123`
- Enter username: `john.bsky.social`
- Enter score: `50`

View top users:
- Choose option 3
- Enter how many to display: `5`

## Troubleshooting

**"SyntaxError: invalid syntax" at line with `print(f"Error: {e}", file=sys.stderr)`**
- This means you're using Python 2.x instead of Python 3
- Solution: Use `python3 main.py` instead of `python main.py`
- Check your version: `python3 --version` (should be 3.7+)
- Your system's `python` command points to Python 2.7

**"ModuleNotFoundError: No module named 'rich'"**
- Run: `pip3 install -r requirements.txt`
- Or: `pip install -r requirements.txt` (if pip is Python 3)

**How to check which Python you're using:**
```bash
python --version    # Might be Python 2.7
python3 --version   # Should be Python 3.7+
```

## Database Location

The default database file is `bluesky_data.json` in the current directory.

You can view or edit it directly - it's just a JSON file!

Example structure:
```json
{
  "users": [
    {"username": "alice.bsky.social", "score": 100}
  ],
  "posts": [
    {
      "link": "https://bsky.app/profile/alice.bsky.social/post/1",
      "username": "alice.bsky.social",
      "score": 50
    }
  ]
}
```
