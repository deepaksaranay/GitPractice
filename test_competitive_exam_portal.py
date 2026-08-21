from competitive_exam_portal import CATEGORIES, QUESTION_BANK, generate_exam, score_exam


def make_questions():
    return [
        {"category": "General Knowledge", "question": "Q1?", "options": ["A", "B", "C", "D"], "answer": 1},
        {"category": "General Knowledge", "question": "Q2?", "options": ["A", "B", "C", "D"], "answer": 2},
        {"category": "General Knowledge", "question": "Q3?", "options": ["A", "B", "C", "D"], "answer": 0},
    ]


def test_generate_exam_respects_num_questions():
    exam = generate_exam(QUESTION_BANK, num_questions=5)
    assert len(exam) == 5


def test_generate_exam_filters_by_category():
    exam = generate_exam(QUESTION_BANK, category="English Language", num_questions=20)
    assert len(exam) > 0
    assert all(q["category"] == "English Language" for q in exam)


def test_generate_exam_caps_at_available_questions():
    exam = generate_exam(QUESTION_BANK, category="English Language", num_questions=1000)
    available = [q for q in QUESTION_BANK if q["category"] == "English Language"]
    assert len(exam) == len(available)


def test_generate_exam_all_categories_when_none_selected():
    exam = generate_exam(QUESTION_BANK, category="All Categories", num_questions=1000)
    assert len(exam) == len(QUESTION_BANK)


def test_score_exam_all_correct():
    questions = make_questions()
    answers = {"0": "1", "1": "2", "2": "0"}
    result = score_exam(questions, answers)
    assert result["correct"] == 3
    assert result["total"] == 3
    assert result["percentage"] == 100.0
    assert result["passed"] is True


def test_score_exam_all_wrong():
    questions = make_questions()
    answers = {"0": "0", "1": "0", "2": "1"}
    result = score_exam(questions, answers)
    assert result["correct"] == 0
    assert result["percentage"] == 0.0
    assert result["passed"] is False


def test_score_exam_partial_and_unanswered():
    questions = make_questions()
    answers = {"0": "1"}
    result = score_exam(questions, answers)
    assert result["correct"] == 1
    assert result["total"] == 3
    assert round(result["percentage"], 2) == round(100 / 3, 2)
    review_for_unanswered = result["review"][1]
    assert review_for_unanswered["selected_index"] is None
    assert review_for_unanswered["is_correct"] is False


def test_score_exam_pass_threshold():
    questions = make_questions()
    answers = {"0": "1", "1": "2"}
    result = score_exam(questions, answers)
    assert result["percentage"] == round(200 / 3, 2)
    assert result["passed"] is True


def test_categories_are_derived_from_question_bank():
    assert set(CATEGORIES) == {q["category"] for q in QUESTION_BANK}
