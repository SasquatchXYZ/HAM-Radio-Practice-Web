from flask import Flask, render_template
from app.models.questions import Questions

app = Flask(__name__)


@app.route('/')
def index():
    # Call the function and store the returned data in a variable
    my_questions = Questions()
    data = my_questions.connect_to_database()

    # Return the HTML template for the index page
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
