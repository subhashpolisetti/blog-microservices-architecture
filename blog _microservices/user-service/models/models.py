import sqlite3

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_all_users():
        conn = User.get_db_connection()
        rows = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_user_by_id(user_id):
        conn = User.get_db_connection()
        row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_user(name, email):
        conn = User.get_db_connection()
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
