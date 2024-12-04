#!/usr/bin/env python3

""" db_migrate.py
Generates the database schema for all db models
- Initializes Users, Sections, and UserSections tables.
- Imports data from the old database to the new database.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_migrate.py

Or run from the root of the project:
> scripts/db_migrate.py

General Process outline:
0. Warning to the user.
1. Old data extraction.  An API has been created in the old project ...
  - Extract Data: retrieves data from the specified tables in the old database.
  - Transform Data: the API to JSON format understood by the new project.
2. New schema.  The schema is created in "this" new database.
3. Load Data: The bulk load API in "this" project inserts the data using required business logic.

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