import sqlite3

def init_db():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_account(username, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                       (username, password))
        conn.commit()
        conn.close()
        return True # success
    except sqlite3.IntegrityError:
        conn.close()
        return False # failure


def check_account(username, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?',
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
