import random


class Questions:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_questions(self):
        self.cursor.execute("SELECT id FROM questions")  # Adjust SQL query as needed
        return self.cursor.fetchall()

    def get_question_set(self, session_id=None):
        if session_id is None:
            all_questions = self.get_all_questions()
            if len(all_questions) < 35:
                return "There are not enough questions to generate a set."
            question_set = set()
            while len(question_set) < 35:
                question_id = random.choice(list(all_questions))
                question_set.add(question_id)
            return list(question_set)
        else:
            self.cursor.execute("""
                WITH question_set_info AS (
                    SELECT DISTINCT question_id
                    FROM question_sets
                    WHERE session_id = ?
                )
                SELECT
                    questions.id,
                    questions.correct,
                    questions.question,
                    questions.a,
                    questions.b,
                    questions.c,
                    questions.d
                    FROM questions
                    JOIN question_set_info
                    ON questions.id = question_set_info.question_id;"""
                                , (session_id,))
            result = self.cursor.fetchall()
            if result is None:
                return None
            else:
                return list(result)
