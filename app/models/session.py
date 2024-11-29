from .questions import Questions


class Session:
    def __init__(self, cursor):
        self.cursor = cursor
        self.session_id = self.create_session()
        self.questions_correct = 0
        self.questions_incorrect = 0

    def create_session(self):
        self.cursor.execute("SELECT MAX(session_id) FROM sessions")
        result = self.cursor.fetchone()
        if result[0] is None:
            session_id = 1
        else:
            session_id = result[0] + 1
        self.cursor.execute("INSERT INTO sessions VALUES (?, ?, ?)", (session_id, 0, 0))
        question_set_id = self.create_question_set(session_id)
        return session_id

    def create_question_set(self, session_id):
        questions = Questions(self.cursor)
        question_set_id = 1
        question_set = questions.get_question_set(35)
        for question in question_set:
            self.cursor.execute("INSERT INTO question_sets VALUES (?, ?, ?)",
                                (question_set_id, session_id, question[0]))
            question_set_id += 1
        return question_set_id
