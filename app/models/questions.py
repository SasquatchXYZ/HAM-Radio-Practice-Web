import random


class Questions:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_questions(self):
        self.cursor.execute("SELECT id FROM questions")  # Adjust SQL query as needed
        return self.cursor.fetchall()

    def get_question_set(self):
        all_questions = self.get_all_questions()
        if len(all_questions) < 35:
            return "There are not enough questions to generate a set."
        question_set = set()
        while len(question_set) < 35:
            question_id = random.choice(list(all_questions))
            question_set.add(question_id)
        return list(question_set)
