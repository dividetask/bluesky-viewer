# Quick Start Guide

## Prerequisites

**Python 3.7 or higher required** - This will NOT work with Python 2.x

Check your Python version:
```bash
python3 --version
```

## Installation

**Easy installation** (handles broken pip automatically):

```bash
./install.sh
```

This creates a virtual environment and installs all dependencies. It works even if your system's pip is broken!

**After installation, run the viewer:**

```bash
./run.sh
```

---

<details>
<summary>Alternative: Manual installation (click to expand)</summary>

If you prefer to install manually or the script doesn't work:

```bash
# Create virtual environment
python3.11 -m venv venv --without-pip

# Bootstrap pip in the venv
venv/bin/python3 -m ensurepip --upgrade

# Install dependencies
venv/bin/python3 -m pip install -r requirements.txt

# Run the viewer
venv/bin/python3 main.py
```

</details>

## First Steps

Once installed, start the viewer:

```bash
./run.sh
```

Try these options:

1. **Option 3** - Browse Top Posts from Bluesky (Start here!)
2. **Option 1** - View all saved users
3. **Option 2** - View all saved posts

## Example Usage

Browse Bluesky posts:
- Choose option 3
- The viewer will fetch popular posts from Bluesky
- Read through posts and their authors
- When you find an interesting post, answer "yes" to add it to your database
- The author will be automatically added to your user list
- Continue browsing or press "no" to stop

View your saved data:
- Choose option 1 to see all users you've tracked
- Choose option 2 to see all posts you've saved

## Troubleshooting

**"SyntaxError: invalid syntax" at line with `print(f"Error: {e}", file=sys.stderr)`**
- This means you're using Python 2.x instead of Python 3
- Solution: Use `python3 main.py` instead of `python main.py`
- Check your version: `python3 --version` (should be 3.7+)
- Your system's `python` command points to Python 2.7

**"ModuleNotFoundError: No module named 'rich'" or "No module named 'atproto'"**
- Run: `python3 -m pip install -r requirements.txt --user`
- Or use the install script: `./install.sh`
- This installs all required dependencies including rich, atproto, and others

**"AttributeError: module 'lib' has no attribute 'X509_V_FLAG_NOTIFY_POLICY'" when running pip3**
- Your system's pip3 is broken due to OpenSSL issues
- Solution: Use `python3 -m pip` instead of `pip3`
- Example: `python3 -m pip install -r requirements.txt --user`
- Or just run: `./install.sh`

**"ModuleNotFoundError: No module named '_cffi_backend'"**
- Run: `pip3 install --ignore-installed cffi`
- This fixes a dependency issue with the cryptography library

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
