import sqlite3


class DatabaseConnection:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
