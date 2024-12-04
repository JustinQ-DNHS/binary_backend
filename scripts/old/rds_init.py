
import psycopg2

rds_host = 'kasm-student-db-instance.ctenoof0kzic.us-east-2.rds.amazonaws.com'
rds_port = '3306'
rds_user = 'kasm_admin'
rds_password = 'pZTXfhhcvuqkF2vEy27x'

# ENTER THE NEW DB NAME
new_db_name = 'new_database_name'

conn = psycopg2.connect(
    dbname='postgres',  #  change according to new db requirements
    user=rds_user,
    password=rds_password,
    host=rds_host,
    port=rds_port
)
conn.autocommit = True  # enable autocommit 
cursor = conn.cursor()

#  new database creation
cursor.execute(f'CREATE DATABASE {new_db_name}')
print(f'Database {new_db_name} created successfully.')

cursor.close()
conn.close()

# connect to the new database
conn = psycopg2.connect(
    dbname=new_db_name,
    user=rds_user,
    password=rds_password,
    host=rds_host,
    port=rds_port
)
cursor = conn.cursor()

# creating the tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    _name TEXT,
    _uid TEXT,
    _password TEXT,
    _role TEXT,
    _pfp TEXT,
    kasm_server_needed BOOLEAN,
    status INTEGER
)
''')
print("Table 'users' created successfully.")

cursor.execute('''
CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY,
    _name TEXT,
    _abbreviation TEXT
)
''')
print("Table 'sections' created successfully.")

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_sections (
    user_id INTEGER,
    section_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(section_id) REFERENCES sections(id)
)
''')
print("Table 'user_sections' created successfully.")

conn.commit()
cursor.close()
conn.close()
print("Schema applied successfully.")
