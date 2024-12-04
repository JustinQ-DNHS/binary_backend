import psycopg2
import json

rds_host = 'kasm-student-db-instance.ctenoof0kzic.us-east-2.rds.amazonaws.com'
rds_port = '3306'
rds_user = 'kasm_admin'
rds_password = 'pZTXfhhcvuqkF2vEy27x'

# Name of new db
new_db_name = 'new_database_name'

# connect to the new RDS database (new one that was just created)
conn = psycopg2.connect(
    dbname=new_db_name,
    user=rds_user,
    password=rds_password,
    host=rds_host,
    port=rds_port
)
cursor = conn.cursor()

# read JSON data from file
with open('data_dump.json') as json_file:
    data = json.load(json_file)

# inset data into NEW 'users' table
for user in data['users']:
    cursor.execute('''
    INSERT INTO users (_name, _uid, _password, _role, _pfp, kasm_server_needed, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (user['_name'], user['_uid'], user['_password'], user['_role'], user['_pfp'], user['kasm_server_needed'], user['status']))

print("Data inserted into 'users' table.")

# inset data into NEW 'sections' table
for section in data['sections']:
    cursor.execute('''
    INSERT INTO sections (_name, _abbreviation)
    VALUES (%s, %s)
    ''', (section['_name'], section['_abbreviation']))

print("Data inserted into 'sections' table.")

# insert data into  NEW 'user_sections' table
for user_section in data['user_sections']:
    cursor.execute('''
    INSERT INTO user_sections (user_id, section_id)
    VALUES (%s, %s)
    ''', (user_section['user_id'], user_section['section_id']))

print("Data inserted into 'user_sections' table.")

# commit  transaction , close the connection
conn.commit()
cursor.close()
conn.close()
print("Data successfully updated in the new database.")
