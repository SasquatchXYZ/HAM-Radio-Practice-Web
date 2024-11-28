import sqlite3


class Questions:
    def __init__(self):
        # Connect to the database
        self.connect_to_database()
        pass

    def connect_to_database(self):
        # TODO: Implement database connection logic
        # Connect to a SQLite database.  The file name is data/questions.db
        connection = sqlite3.connect('data/questions.db')

        # Create a cursor object
        cursor = connection.cursor()

        # Define your query
        query = "SELECT * FROM questions"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Close the connection
        connection.close()

        # Print the results
        for row in results:
            print(row)

    def update_database(self):
        # TODO: Implement database update logic
        pass

    def validate_and_cleanse_data(self):
        # TODO: Implement data validation and cleansing logic
        pass

    def fetch_questions(self):
        # TODO: Implement logic to fetch questions from the database
        pass
