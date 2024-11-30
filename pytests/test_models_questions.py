# Generated from inside the test file
import sqlite3
import pytest

from app.models.questions import Questions


# import pytest
# from models.questions import Question  # Adjust the import according to the actual module contents


# Example Test Class
class TestQuestion:

    @pytest.fixture(scope="module")
    def db_connection(self):
        # Setup: create the in-memory database connection
        memory_connection = self.create_in_memory_db_from_existing('../data/questions.db')
        yield memory_connection  # This is where the testing happens

        # Teardown: Close the database connection
        memory_connection.close()

    def test_connection(self, db_connection: sqlite3.Connection):
        # Execute a SQL query to count the number of records in the questions table
        cursor = db_connection.execute("SELECT COUNT(*) FROM questions")
        # Fetch the result of the query
        count = cursor.fetchone()[0]
        # Assert that the count matches the expected number of records
        expected_count = 411  # Replace with the expected number of records
        assert count == expected_count, f"Expected {expected_count} records, but found {count}"

    def test_get_questions(self, db_connection: sqlite3.Connection):
        # Example test using the db_connection fixture
        result = db_connection.execute("SELECT * FROM questions WHERE id = 'T1A01'")
        question = result.fetchone()
        assert question is not None

    def test_get_question_set(self, db_connection: sqlite3.Connection):
        questions = Questions(db_connection.cursor())

        # Call the get_question_set method with no session_id
        question_set = questions.get_question_set()

        # Verify the results
        assert question_set is not None
        assert len(question_set) > 0  # Assuming it returns a list of questions

    def test_get_all_questions_empty_list(self, db_connection: sqlite3.Connection):
        # Arrange
        # Clear the questions table
        db_connection.execute("DELETE FROM questions")
        db_connection.commit()

        # Act
        result = Questions(db_connection.cursor()).get_all_questions()

        # Assert
        assert result == []

    #     def setup_method(self):
    #         """Setup any state specific to the execution of the given module."""
    #         # Initialize any resources you might need
    #         self.example_data = {
    #             'title': 'Example Question',
    #             'content': 'What is the meaning of life?',
    #             # Add other fields as necessary
    #         }
    #
    #     def test_question_creation(self):
    #         """Test the creation of a Question instance."""
    #         question = Question(**self.example_data)
    #         assert question.title == 'Example Question'
    #         assert question.content == 'What is the meaning of life?'
    #
    #     def test_question_method(self):
    #         """Test a specific method of the Question class."""
    #         question = Question(**self.example_data)
    #         result = question.some_method()  # Replace with an actual method
    #         assert result == expected_value  # Replace with expected output
    #
    #     @pytest.mark.parametrize("input_data,expected", [
    #         # Add tuples of (input, expected_output)
    #         ({'title': 'Hello', 'content': 'World'}, 'Expected Result'),  # Example pair
    #     ])
    #     def test_question_parametrized(self, input_data, expected):
    #         """Test with multiple parameter sets."""
    #         question = Question(**input_data)
    #         result = question.some_method()  # Replace with an actual method
    #         assert result == expected

    def create_in_memory_db_from_existing(self, existing_db_path: str):
        # Connect to the existing database
        existing_conn = sqlite3.connect(existing_db_path)
        existing_cursor = existing_conn.cursor()

        # Extract the schema from the existing database
        existing_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name IS NOT 'sqlite_sequence'")
        schema_statements = existing_cursor.fetchall()

        # Connect to the in-memory database
        memory_conn = sqlite3.connect(":memory:")
        memory_cursor = memory_conn.cursor()

        # Apply the schema to the in-memory database
        for statement in schema_statements:
            if statement[0]:  # Ensure the statement is not None
                memory_cursor.execute(statement[0])

        # Optionally, copy data from the existing database to the in-memory database
        for table_info in existing_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            table_name = table_info[0]
            if table_name != 'sqlite_sequence':  # Skip the sqlite_sequence table
                data = existing_cursor.execute(f"SELECT * FROM {table_name}").fetchall()
                columns = [description[0] for description in existing_cursor.description]
                placeholders = ', '.join(['?'] * len(columns))
                memory_cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
                                          data)

        # Commit changes to the in-memory database
        memory_conn.commit()

        # Close the existing database connection
        existing_conn.close()

        return memory_conn
