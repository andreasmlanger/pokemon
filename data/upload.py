"""
Uploads json data to Elephant SQL database
"""

import psycopg2
import json
import os


TABLE_NAME = 'Pokemon'  # table name in database


def upload_pokemon_json_to_database(json_path):
    conn = establish_connection()  # connect to Elephant SQL database
    delete_table(conn)
    create_new_table(conn)
    load_pokemon_into_table(conn, json_path=json_path)
    conn.close()


def establish_connection():
    conn = psycopg2.connect(
        user=os.environ.get('SQL_NAME'),
        password=os.environ.get('SQL_PASSWORD'),
        host=os.environ.get('SQL_HOST'),
        port='5432',
        database=os.environ.get('SQL_NAME'),
    )
    print('Connection to database')
    return conn


def delete_table(conn):
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {TABLE_NAME};')
    conn.commit()
    cur.close()
    print(f'Table "{TABLE_NAME}" deleted successfully!')


def create_new_table(conn):
    cur = conn.cursor()
    query = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            idx INTEGER,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            form VARCHAR(255),
            caught BOOLEAN
        );
        '''
    cur.execute(query)
    conn.commit()
    cur.close()
    print(f'Table "{TABLE_NAME}" created successfully!')


def load_pokemon_into_table(conn, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    cur = conn.cursor()
    q = f'INSERT INTO {TABLE_NAME} (idx, name, type, form, caught) VALUES (%s, %s, %s, %s, %s);'
    arguments = [(row['idx'], row['name'], row['type'], row.get('form', None), False) for row in data]
    cur.executemany(q, arguments)
    conn.commit()
    cur.close()
    print('Data successfully added!')
