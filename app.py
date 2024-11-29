from flask import Flask, render_template, request
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # Check if the form has been submitted
    if request.method == 'POST':
        # Start the question session
        # ...
        db_path = 'data/questions.db'
        # Call the fucntion and store the returned data in a variable
        with DatabaseConnection(db_path) as cursor:
            session = Session(cursor)
            print("Session ID:", session.session_id)
            questions = Questions(cursor)
            data = questions.get_question_set()
    else:
        data = None
    # Return the HTML template for the index page
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
