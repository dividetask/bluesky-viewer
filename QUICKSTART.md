# Quick Start Guide

## Prerequisites

**Python 3.7 or higher required** - This will NOT work with Python 2.x

Check your Python version:
```bash
python3 --version
```

## Installation

1. **Install dependencies:**

   **Easy way** (recommended):
   ```bash
   ./install.sh
   ```

   **Or manually:**
   ```bash
   python3 -m pip install -r requirements.txt --user
   ```

   **If you have a working pip3:**
   ```bash
   pip3 install -r requirements.txt
   ```

   **Note:** If `pip3` gives you errors about OpenSSL or AttributeError, use `python3 -m pip` instead. This is a common issue on some systems.

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
