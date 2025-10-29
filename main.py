#!/usr/bin/env python3
"""
Bluesky Terminal Viewer - Main Entry Point
A simple terminal-based viewer for Bluesky users and posts
"""

import sys
import argparse
from viewer import BlueskyViewer


def main():
    parser = argparse.ArgumentParser(
        description="Bluesky Terminal Viewer - View and manage Bluesky users and posts"
    )
    parser.add_argument(
        "--db",
        type=str,
        default="bluesky_data.json",
        help="Path to the JSON database file (default: bluesky_data.json)"
    )

    args = parser.parse_args()

    try:
        viewer = BlueskyViewer(db_path=args.db)
        viewer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
