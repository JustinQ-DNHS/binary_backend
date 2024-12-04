#!/usr/bin/env python3

""" db_backup.py
Backs up the current database and saves the data to JSON files.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_backup.py

Or run from the root of the project:
> scripts/db_backup.py
"""

import sys
import os

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, backup_data

def main():
    # Step 1: Backup the old database
    with app.app_context():
        backup_data()

if __name__ == "__main__":
    main()