import sqlite3

def establish_connection():
    return sqlite3.connect('database/report.db')

def close_connection(conn):
    if conn:
        conn.close()