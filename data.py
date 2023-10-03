import sqlite3
import pandas as pd
from data import *


DB_FILE = 'companies.db'

def connect_to_db(db_file):
    return sqlite3.connect(db_file)

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            id INTEGER PRIMARY KEY,
            Bolag TEXT UNIQUE,
            Bonusinformation TEXT,
            Koncern TEXT
        )
    ''')

def fetch_data(cursor):
    cursor.execute('SELECT Bolag, Bonusinformation, Koncern FROM Companies')
    rows = cursor.fetchall()
    return {
        'Bolag': [row[0] for row in rows],
        'Bonusinformation': [row[1] for row in rows],
        'Koncern': [row[2] for row in rows]
    }

def fetch_data_as_dataframe(conn):
    sql_query = 'SELECT Bolag, Bonusinformation, Koncern FROM Companies'
    return pd.read_sql_query(sql_query, conn)

def refresh_data():
    global df, data  # Declare df and data as global variables
    with connect_to_db(DB_FILE) as conn:
        df = fetch_data_as_dataframe(conn)
    with connect_to_db(DB_FILE) as conn:
        cursor = conn.cursor()
        data = fetch_data(cursor)

def add_company(bolag, bonusinformation, koncern):
    with connect_to_db(DB_FILE) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Companies (Bolag, Bonusinformation, Koncern) VALUES (?, ?, ?)', (bolag, bonusinformation, koncern))
            conn.commit()
            refresh_data()  # Refresh df and data after adding a company
        except sqlite3.IntegrityError:
            print(f"Company {bolag} already exists in the database.")

def delete_company(bolag):
    with connect_to_db(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Companies WHERE Bolag = ?', (bolag,))
        conn.commit()
        refresh_data()  # Refresh df and data after deleting a company

# delete_company('OldCo')


def df_data():        
    with connect_to_db(DB_FILE) as conn:
        df = fetch_data_as_dataframe(conn)
        
    with connect_to_db(DB_FILE) as conn:
        cursor = conn.cursor()
        data = fetch_data(cursor)
    
    return df, data



df, data = df_data()
