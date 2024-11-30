# File: test_questions.py
# Generated using Jetbrains AI from the Questions class

import pytest
from app.models.questions import Questions
from unittest.mock import MagicMock


@pytest.fixture
def setup_questions():
    mock_cursor = MagicMock()
    questions = Questions(mock_cursor)
    return questions, mock_cursor


def test_get_all_questions(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]
    result = questions.get_all_questions()
    assert result == [(1,), (2,), (3,)]
    mock_cursor.execute.assert_called_with("SELECT id FROM questions")


def test_get_question_with_valid_id(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = (1, 'a', 'Example Question?', 'a', 'b', 'c', 'd')
    result = questions.get_question(1)
    expected = {'id': 1, 'correct': 'a', 'question': 'Example Question?', 'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'}
    assert result == expected


def test_get_question_with_invalid_id(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = None
    result = questions.get_question(999)
    assert result is None


def test_get_question_set_without_session_id(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchall.return_value = list(range(100))
    result = questions.get_question_set()
    assert len(result) == 35
    mock_cursor.execute.assert_called_with("SELECT id FROM questions")


def test_get_question_set_with_insufficient_questions(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchall.return_value = []
    result = questions.get_question_set()
    assert result == "There are not enough questions to generate a set."


def test_get_answered_questions(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = (5, 2)
    result = questions.get_answered_questions(1)
    assert result == 7
    mock_cursor.execute.assert_called_with(
        "SELECT questions_correct, questions_incorrect FROM sessions WHERE session_id = ?", (1,))


def test_get_next_question_before_35(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchall.side_effect = [[(1,), (2,), (3,)], [(5,)]]
    result = questions.get_next_question(1)
    assert result == '5'
    mock_cursor.execute.assert_any_call("SELECT question_id FROM question_sets WHERE session_id = ?", (1,))


def test_store_answer_correct(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = (1,)
    result = questions.store_answer(1, 1, 1)
    assert result == "test"
    mock_cursor.execute.assert_any_call(
        "UPDATE sessions SET questions_correct = questions_correct + 1 WHERE session_id = ?", (1,))


def test_store_answer_incorrect(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = (2,)
    result = questions.store_answer(1, 1, 1)
    assert result == "test"
    mock_cursor.execute.assert_any_call(
        "UPDATE sessions SET questions_incorrect = questions_incorrect + 1 WHERE session_id = ?", (1,))


def test_tally_results(setup_questions):
    questions, mock_cursor = setup_questions
    mock_cursor.fetchone.return_value = (10, 5)
    result = questions.tally_results(1)
    assert result == {"questions_correct": 10, "questions_incorrect": 5}
    mock_cursor.execute.assert_called_with(
        "SELECT questions_correct, questions_incorrect FROM sessions WHERE session_id = ?", (1,))
