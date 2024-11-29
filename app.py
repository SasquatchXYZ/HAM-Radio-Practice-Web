import sqlite3

from flask import Flask, render_template, request, make_response, url_for, redirect
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)


@app.route('/delete-cookie', methods=['GET'])
@app.before_request
def before_request():
    if request.endpoint == 'delete-cookie':
        response = make_response(render_template('index.html', data=None, session_id=None))
        response.delete_cookie('session_id')
        return response


@app.route('/quiz/<question_id>/<question_number>', methods=['GET', 'POST'])
def quiz(question_id, question_number):
    current_session = request.cookies.get('session_id')
    this_question = None
    # Set the path to the database
    db_path = 'data/questions.db'
    # Call the function and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:
        if isinstance(cursor, sqlite3.Cursor):
            # The 'cursor' object is a valid database cursor
            questions = Questions(cursor)  # Assuming 'cursor' is your database cursor
            print("question_id: " + question_id)
            this_question = questions.get_question(question_id)
        else:
            # The 'cursor' object is not a valid database cursor
            print("Error: 'cursor' object is not a valid database cursor")

        # next_question = questions.get_next_question(current_session)
        if request.method == 'POST':
            selected_answer = request.form['answer']
            questions.store_answer(question_id, selected_answer, current_session)
            questions_answered = questions.get_answered_questions(current_session)

            if questions_answered < 35:
                next_question = questions.get_next_question(current_session)
                print("next question: " + next_question)
                question_number = int(question_number) + 1
                return redirect(url_for('quiz', question_id=next_question, question_number=str(question_number)))
            else:
                return redirect(url_for('results'))

        return render_template('quiz.html', question=this_question, question_number=question_number)


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


@app.route('/results', methods=['GET'])
def results():
    db_path = 'data/questions.db'

    with DatabaseConnection(db_path) as cursor:
        if isinstance(cursor, sqlite3.Connection):
            questions = Questions(cursor)
            current_session = request.cookies.get('session_id')
            final_results = questions.tally_results(current_session)
            print(current_session)
            print(final_results)
            correct = final_results['questions_correct']
            incorrect = final_results['questions_incorrect']
            total_answered = correct + incorrect

    # Create a response object
    response = make_response(
        render_template('results.html', correct=correct, incorrect=incorrect, total_answered=total_answered))

    # Delete the 'session_id' cookie
    response.delete_cookie('session_id')

    return response


if __name__ == '__main__':
    app.run(debug=True)
