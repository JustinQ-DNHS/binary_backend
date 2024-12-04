#!/usr/bin/env python3

""" db_restore.py
Restores the database from JSON files.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_restore.py

Or run from the root of the project:
> scripts/db_restore.py
"""

import sys
import os

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, restore_data_command

def main():
    # Step 3: Restore the database
    with app.app_context():
        restore_data_command()

if __name__ == "__main__":
    main()