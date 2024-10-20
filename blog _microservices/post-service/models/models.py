import sqlite3

class Post:
    def __init__(self, id, title, content, user_id):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_all_posts():
        conn = Post.get_db_connection()
        rows = conn.execute('SELECT * FROM posts').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_post_by_id(post_id):
        conn = Post.get_db_connection()
        row = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_post(title, content, user_id):
        conn = Post.get_db_connection()
        conn.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)', (title, content, user_id))
        conn.commit()
        conn.close()
