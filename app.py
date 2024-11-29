from flask import Flask, render_template, request, make_response
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    db_path = 'data/questions.db'
    # Call the function and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:
        session = Session(cursor)
        current_session = request.cookies.get('session_id')
        if current_session is None:
            questions = Questions(cursor)
            data = questions.get_question_set()
            session.session_id = session.create_session()
            response = make_response(render_template('index.html', data=data, session_id=session.session_id))
            response.set_cookie('session_id', str(session.session_id))
            return response
        else:
            # We have a cookie value and existing id
            session.session_id = current_session
            questions = Questions(cursor)
            data = questions.get_question_set()
            response = make_response(render_template('index.html', data=data, session_id=session.session_id))
            return response


if __name__ == '__main__':
    app.run(debug=True)
