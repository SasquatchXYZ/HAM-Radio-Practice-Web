class Questions:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM questions")  # Adjust SQL query as needed
        return self.cursor.fetchall()
