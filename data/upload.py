"""
Uploads json data to PostgreSQL database
"""

import psycopg2
from psycopg2.extras import DictCursor
import json
import os


TABLE_NAME = 'pokemon'  # table name in database


def upload_pokemon_json_to_database(json_path):
    conn = establish_connection()  # connect to PostgreSQL database
    verify_successful_connection(conn)
    if check_if_table_exists(conn, TABLE_NAME):
        update_json_from_db(conn, json_path)
    delete_table(conn)
    create_new_table(conn)
    load_pokemon_into_table(conn, json_path=json_path)
    conn.close()


def establish_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRESQL_DBNAME'),
        host=os.environ.get('POSTGRESQL_HOST'),
        port=os.environ.get('POSTGRESQL_PORT'),
        user=os.environ.get('POSTGRESQL_USER'),
        password=os.environ.get('POSTGRESQL_PASSWORD')
    )
    return conn


def verify_successful_connection(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    record = cursor.fetchone()
    print('Connected to - ', record)


def check_if_table_exists(conn, name):
    cur = conn.cursor()
    cur.execute(f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{name}')")
    return cur.fetchone()[0]


def drop_all_tables():
    """
    Will reset the complete PostgreSQL database!
    """
    conn = establish_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    for table in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")
    conn.commit()
    cur.close()
    conn.close()
    print('All tables deleted!')
    vacuum()  # vacuum after deleting!


def vacuum():
    conn = establish_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('VACUUM FULL')
    conn.commit()
    cur.close()
    conn.close()
    print('PostgreSQL database vacuumed!')


def open_json(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)


def save_to_json(poke_list, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(poke_list, json_file, indent=2)


def update_json_from_db(conn, json_path):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(f'SELECT * FROM {TABLE_NAME}')
    rows = cur.fetchall()
    cur.close()

    # Save information if Pokémon has been caught in dictionary
    caught_dic = {}
    for row in rows:
        row_dict = dict(row)
        key = f"{row_dict['idx']}_{row_dict['form']}" if row_dict['form'] else row_dict['idx']
        caught_dic[key] = row_dict['caught']

    # Update json
    data = open_json(json_path)
    for d in data:
        key = f"{d['idx']}_{d['form']}" if 'form' in d else d['idx']
        if caught_dic[key]:
            d['caught'] = caught_dic[key]
    save_to_json(data, json_path)
    print(f'JSON updated successfully from database!')


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
    data = open_json(json_path)
    cur = conn.cursor()
    q = f'INSERT INTO {TABLE_NAME} (idx, name, type, form, caught) VALUES (%s, %s, %s, %s, %s);'
    arguments = [(d['idx'], d['name'], d['type'], d.get('form', None), d.get('caught', False)) for d in data]
    cur.executemany(q, arguments)
    conn.commit()
    cur.close()
    print('Pokémon data successfully added to database!')
