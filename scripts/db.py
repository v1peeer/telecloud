import hashlib
import json
import sqlite3
import os
import secrets
from datetime import datetime

class Database:
    def __init__(self, db):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, db)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS file (id text PRIMARY KEY, file_name text, file_path text, file_size integer, chunks text, type text, uploaded text, token text)"  # Add 'token text' here
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password text, token text)"
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM file")
        rows = self.cur.fetchall()
        return rows

    def insert(self, id, file_name, file_path, file_size, chunks, type, token):
        chunks_str = json.dumps(chunks)
        today = datetime.now()
        self.cur.execute(
            "INSERT INTO file VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id, file_name, file_path, file_size, chunks_str, type, today, token),
        )
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM file WHERE id=?", (id,))
        self.conn.commit()

    def get_file(self, id):
        self.cur.execute("SELECT * FROM file WHERE id=?", (id,))
        rows = self.cur.fetchall()
        return rows

    def find_file_by_name_or_path_or_id(self, file_query):
        self.cur.execute(
            "SELECT * FROM file WHERE file_name=? OR file_path=? OR id=? or file_name LIKE ? or file_path LIKE ? or id LIKE ? or type=?",
            (file_query, file_query, file_query, f"%{file_query}%", f"%{file_query}%", f"%{file_query}%", file_query),
        )
        rows = self.cur.fetchall()
        return rows

    def create_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        token = secrets.token_urlsafe(16)
        self.cur.execute(
            "INSERT INTO users VALUES (?, ?, ?)", (username, hashed_password, token)
        )
        self.conn.commit()
        return token

    def get_user(self, username):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cur.fetchone()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, token):
        self.cur.execute("SELECT * FROM users WHERE token=?", (token,))
        return self.cur.fetchone()

    def fetch_files_by_token(self, token):
        self.cur.execute("SELECT * FROM file WHERE token=?", (token,))
        rows = self.cur.fetchall()
        return rows

    def find_file_by_name_or_path_or_id(self, file_query, token):
        self.cur.execute(
            "SELECT * FROM file WHERE (file_name=? OR file_path=? OR id=? or file_name LIKE ? or file_path LIKE ? or id LIKE ? or type=?) AND token=?",
            (file_query, file_query, file_query, f"%{file_query}%", f"%{file_query}%", f"%{file_query}%", file_query, token),
        )
        rows = self.cur.fetchall()
        return rows

    def insert(self, id, file_name, file_path, file_size, chunks, type, token):
        chunks_str = json.dumps(chunks)
        today = datetime.now()
        self.cur.execute(
            "INSERT INTO file VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id, file_name, file_path, file_size, chunks_str, type, today, token),
        )
        self.conn.commit()