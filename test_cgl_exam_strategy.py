import pytest

from cgl_exam_strategy import (
    SECTIONS,
    accuracy,
    generate_study_plan,
    mock_total,
    record_mock,
    section_score,
    should_attempt,
    weak_sections,
)


def make_results():
    return {
        "Quantitative Aptitude": (15, 4),
        "General Intelligence & Reasoning": (22, 1),
        "English Comprehension": (20, 2),
        "General Awareness": (12, 6),
    }


def test_section_score_applies_negative_marking():
    assert section_score(20, 4) == 38


def test_accuracy_handles_no_attempts():
    assert accuracy(0, 0) == 0.0


def test_accuracy_percentage():
    assert accuracy(3, 1) == 75.0


def test_should_attempt_break_even_is_twenty_percent():
    assert should_attempt(0.25)
    assert not should_attempt(0.2)
    assert not should_attempt(0.1)


def test_record_mock_rejects_too_many_attempts():
    mocks = []
    results = make_results()
    results["General Awareness"] = (20, 10)
    with pytest.raises(ValueError):
        record_mock(mocks, "Mock 1", results)
    assert mocks == []


def test_mock_total_sums_all_sections():
    mocks = []
    record_mock(mocks, "Mock 1", make_results())
    assert mock_total(mocks[0]) == 28 + 43.5 + 39 + 21


def test_weak_sections_orders_lowest_score_first():
    mocks = []
    record_mock(mocks, "Mock 1", make_results())
    ranked = [section for section, _, _ in weak_sections(mocks[0])]
    assert ranked[0] == "General Awareness"
    assert ranked[-1] == "General Intelligence & Reasoning"


def test_study_plan_short_window_is_all_revision():
    plan = generate_study_plan(5, list(SECTIONS))
    assert len(plan) == 5
    assert all("mock test" in task for task in plan)


def test_study_plan_rotates_weak_sections_and_adds_weekly_mocks():
    weak_order = ["General Awareness", "Quantitative Aptitude"]
    plan = generate_study_plan(30, weak_order)
    assert len(plan) == 30
    assert "General Awareness" in plan[0]
    assert "Quantitative Aptitude" in plan[1]
    assert plan[6].startswith("Full-length mock test")
    assert plan[-1].startswith("Final revision")


def test_study_plan_empty_for_non_positive_days():
    assert generate_study_plan(0, list(SECTIONS)) == []
