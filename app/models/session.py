import sqlite3
from .database_connection import DatabaseConnection


class Session:
    def __init__(self):
        self.session_id = self.create_session()
        self.questions_correct = 0
        self.questions_incorrect = 0

    def create_session(self):
        connection = DatabaseConnection('data/questions.db')
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(session_id) FROM sessions)")
        result = cursor.fetchone()
        if result[0] is None:
            session_id = 1
        else:
            session_id = result[0] + 1
        cursor.execute("INSERT INTO sessions VALUES (?, ?, ?)", (session_id, 0, 0))
        connection.commit()
        connection.close()
        return session_id
