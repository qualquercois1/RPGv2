import sqlite3
from database import get_connection

class User:
    def __init__(self, username, password, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            print("Erro: Nome de usuário já existe.")
            return False
        except Exception as e:
            print(f"Ocorreu um erro ao salvar o usuário: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def get_user_by_name(cls, username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(user_id=row[0], username=row[1], password=row[2])
        return None