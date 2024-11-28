from flask import Flask, render_template
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions

app = Flask(__name__)


@app.route('/')
def index():
    db_path = 'data/questions.db'
    # Call the fucntion and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:
        questions = Questions(cursor)
        data = questions.fetch_data()
    # Return the HTML template for the index page
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
