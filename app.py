from flask import Flask, render_template, request, make_response, url_for, redirect
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # Set the path to the database
    db_path = 'data/questions.db'

    # Call the function and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:
        session = Session(cursor)
        questions = Questions(cursor)
        current_session = request.cookies.get('session_id')

        if current_session is None:
            session.session_id = session.create_session()
        else:
            session.session_id = current_session

        questions_answered = questions.get_answered_questions(session.session_id)

        if questions_answered < 35:
            next_question = questions.get_next_question(session.session_id)
            response = make_response(
                render_template('start.html', next_question=next_question, session_id=session.session_id))
            # We set the cookie for Session ID every time
            response.set_cookie('session_id', str(session.session_id))
            return response
        else:
            return redirect(url_for('results'))


if __name__ == '__main__':
    app.run(debug=True)
