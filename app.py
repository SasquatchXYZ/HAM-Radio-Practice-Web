from flask import Flask, render_template
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)


@app.route('/')
def index():
    db_path = 'data/questions.db'
    # Call the fucntion and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:
        session = Session(cursor)
        print("Session ID:", session.session_id)
        questions = Questions(cursor)
        data = questions.get_question_set()
    # Return the HTML template for the index page
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
