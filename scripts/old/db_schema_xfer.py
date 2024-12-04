import sqlite3
import os

def get_all_tables(db_path):
    """Get the list of all tables in the SQLite database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def get_schema(db_path, tables):
    """Get the schema for the specified tables from the SQLite database."""
    schema = []
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        placeholders = ','.join('?' for table in tables)
        cursor.execute(f"SELECT name, sql FROM sqlite_master WHERE type='table' AND name IN ({placeholders});", tables)
        schema = cursor.fetchall()
    return schema

def print_schema(schema):
    """Print the schema."""
    for table_name, table_sql in schema:
        print(f"Table name: {table_name}")
        print(f"Schema: {table_sql}\n")

def table_exists(conn, table_name):
    """Check if a table exists in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

def update_table_schema(conn, table_name, table_sql):
    """Update the schema of an existing table."""
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    cursor.execute(table_sql)
    conn.commit()

def build_new_db(new_db_path, schema):
    """Build a new SQLite database using the provided schema."""
    with sqlite3.connect(new_db_path) as conn:
        for table_name, table_sql in schema:
            if table_exists(conn, table_name):
                update_table_schema(conn, table_name, table_sql)
            else:
                cursor = conn.cursor()
                cursor.execute(table_sql)
                conn.commit()

# Paths to the old and new databases
old_db_path = 'instance/volumes/sqlite.db'
new_db_path = 'instance/volumes/sqlite_v2.db'

# Exclusion list of tables not to transfer
exclusion_list = ['old_table1', 'old_table2']  # dummy tables 

# List of tables to transfer
tables_to_transfer = [table for table in get_all_tables(old_db_path) if table not in exclusion_list]

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(new_db_path), exist_ok=True)

# Get the schema from the old database for the specified tables
schema = get_schema(old_db_path, tables_to_transfer)

# Build the new database with the extracted schema
build_new_db(new_db_path, schema)

print(f"New database created successfully at {new_db_path}.")
new_tables = get_all_tables(new_db_path)
new_schema = get_schema(new_db_path, new_tables)
print("New database schema:")
print_schema(new_schema)