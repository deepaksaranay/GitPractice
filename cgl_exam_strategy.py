SECTIONS = {
    "Quantitative Aptitude": {
        "questions": 25,
        "target_minutes": 18,
        "tips": [
            "Master tables up to 30, squares up to 50 and cubes up to 25.",
            "Revise percentage-fraction equivalents; they speed up Profit & Loss and DI.",
            "Attempt Arithmetic first, then Algebra/Geometry/Trigonometry.",
            "Skip lengthy calculations on the first pass and return to them later.",
        ],
    },
    "General Intelligence & Reasoning": {
        "questions": 25,
        "target_minutes": 12,
        "tips": [
            "Start with this section - it is the quickest to score in.",
            "Practise series, coding-decoding and analogy daily for speed.",
            "For figure-based questions, eliminate options instead of solving fully.",
            "Leave a question if it takes more than 60 seconds.",
        ],
    },
    "English Comprehension": {
        "questions": 25,
        "target_minutes": 12,
        "tips": [
            "Read editorials daily to improve comprehension speed.",
            "Learn 10 new words, idioms or phrases every day and revise weekly.",
            "Revise grammar rules for error spotting and sentence improvement.",
            "Do vocabulary questions first - they take only a few seconds each.",
        ],
    },
    "General Awareness": {
        "questions": 25,
        "target_minutes": 8,
        "tips": [
            "Answer only what you know - guessing here costs negative marks.",
            "Cover the last 6-8 months of current affairs.",
            "Revise static GK (History, Polity, Geography, Science) from one source repeatedly.",
            "Finish this section quickly and spend the saved time on Quant.",
        ],
    },
}

MARKS_PER_CORRECT = 2
NEGATIVE_MARKS = 0.5
TOTAL_MINUTES = 60

mock_tests = []


def section_score(correct, wrong):
    return correct * MARKS_PER_CORRECT - wrong * NEGATIVE_MARKS


def accuracy(correct, wrong):
    attempted = correct + wrong
    if attempted == 0:
        return 0.0
    return round(correct / attempted * 100, 2)


def should_attempt(success_probability):
    expected = success_probability * MARKS_PER_CORRECT - (1 - success_probability) * NEGATIVE_MARKS
    return expected > 0


def record_mock(mocks, name, results):
    for section, (correct, wrong) in results.items():
        if correct + wrong > SECTIONS[section]["questions"]:
            raise ValueError(f"{section}: attempts exceed {SECTIONS[section]['questions']} questions")
    mocks.append({"name": name, "results": results})


def mock_total(mock):
    return sum(section_score(correct, wrong) for correct, wrong in mock["results"].values())


def weak_sections(mock):
    ranked = []
    for section, (correct, wrong) in mock["results"].items():
        ranked.append((section, section_score(correct, wrong), accuracy(correct, wrong)))
    ranked.sort(key=lambda item: (item[1], item[2]))
    return ranked


def generate_study_plan(days_left, weak_order):
    if days_left <= 0:
        return []
    if days_left <= 7:
        return ["Revision + one full mock test daily; analyse every mistake." for _ in range(days_left)]

    plan = []
    for day in range(1, days_left + 1):
        if day % 7 == 0:
            plan.append("Full-length mock test + detailed analysis")
        elif day > days_left - 7:
            plan.append("Final revision: formulas, vocabulary and current affairs notes")
        else:
            focus = weak_order[(day - 1) % len(weak_order)]
            plan.append(f"Focus on {focus} + 1 sectional test + 30 min current affairs")
    return plan


if __name__ == "__main__":
    while True:
        print("\n===== SSC CGL Exam Strategy Planner =====")
        print("1. View Tier 1 Exam Pattern")
        print("2. Section-wise Strategy Tips")
        print("3. Record Mock Test Result")
        print("4. Analyse Mock Tests")
        print("5. Generate Study Plan")
        print("6. Attempt-or-Skip Calculator")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"\nTier 1: {TOTAL_MINUTES} minutes, +{MARKS_PER_CORRECT} per correct, "
                  f"-{NEGATIVE_MARKS} per wrong")
            for section, info in SECTIONS.items():
                print(f"- {section}: {info['questions']} questions, "
                      f"{info['questions'] * MARKS_PER_CORRECT} marks, "
                      f"target time {info['target_minutes']} min")
            print("Always check the latest official SSC notification for pattern changes.")

        elif choice == "2":
            for section, info in SECTIONS.items():
                print(f"\n{section}")
                for tip in info["tips"]:
                    print(f"  * {tip}")

        elif choice == "3":
            name = input("Enter mock test name: ")
            results = {}
            for section in SECTIONS:
                correct = int(input(f"{section} - correct answers: "))
                wrong = int(input(f"{section} - wrong answers: "))
                results[section] = (correct, wrong)

            try:
                record_mock(mock_tests, name, results)
                print("Mock test recorded successfully!")
            except ValueError as error:
                print(f"Invalid data: {error}")

        elif choice == "4":
            if len(mock_tests) == 0:
                print("No mock tests found.")
            else:
                for mock in mock_tests:
                    print(f"\n{mock['name']}: {mock_total(mock)} / 200")
                    for section, score, acc in weak_sections(mock):
                        print(f"  {section}: {score} marks, {acc}% accuracy")
                weakest = weak_sections(mock_tests[-1])[0][0]
                print(f"\nWeakest section in latest mock: {weakest}")

        elif choice == "5":
            days_left = int(input("Days left for the exam: "))
            if mock_tests:
                weak_order = [section for section, _, _ in weak_sections(mock_tests[-1])]
            else:
                weak_order = list(SECTIONS)

            plan = generate_study_plan(days_left, weak_order)
            if not plan:
                print("No study plan found. Enter a positive number of days.")
            else:
                for day, task in enumerate(plan, start=1):
                    print(f"Day {day}: {task}")

        elif choice == "6":
            probability = float(input("Chance your answer is correct (0-100%): ")) / 100
            if should_attempt(probability):
                print("Attempt it - the expected score is positive.")
            else:
                print("Skip it - the expected score is negative.")

        elif choice == "7":
            print("All the best for your SSC CGL exam!")
            break

        else:
            print("Invalid choice!")
