import html
import random
import uuid
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

QUESTION_BANK = [
    {"category": "General Knowledge", "question": "Who is known as the Father of the Nation in India?",
     "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "Sardar Patel"], "answer": 1},
    {"category": "General Knowledge", "question": "Which is the largest planet in the solar system?",
     "options": ["Earth", "Saturn", "Jupiter", "Neptune"], "answer": 2},
    {"category": "General Knowledge", "question": "The Reserve Bank of India was established in which year?",
     "options": ["1935", "1947", "1950", "1969"], "answer": 0},
    {"category": "General Knowledge", "question": "Which gas do plants absorb from the atmosphere for photosynthesis?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2},
    {"category": "General Knowledge", "question": "Who wrote the Indian national anthem?",
     "options": ["Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sarojini Naidu", "Muhammad Iqbal"], "answer": 1},

    {"category": "Quantitative Aptitude", "question": "What is 15% of 200?",
     "options": ["20", "25", "30", "35"], "answer": 2},
    {"category": "Quantitative Aptitude", "question": "If a train travels 60 km in 45 minutes, what is its speed in km/h?",
     "options": ["70", "75", "80", "85"], "answer": 2},
    {"category": "Quantitative Aptitude", "question": "What is the next number in the series: 2, 6, 12, 20, 30, ?",
     "options": ["36", "40", "42", "44"], "answer": 2},
    {"category": "Quantitative Aptitude", "question": "The simple interest on Rs. 1000 at 10% per annum for 2 years is:",
     "options": ["Rs. 100", "Rs. 150", "Rs. 200", "Rs. 250"], "answer": 2},
    {"category": "Quantitative Aptitude", "question": "What is the square root of 144?",
     "options": ["10", "11", "12", "13"], "answer": 2},

    {"category": "Logical Reasoning", "question": "Find the odd one out: Dog, Cat, Lion, Snake",
     "options": ["Dog", "Cat", "Lion", "Snake"], "answer": 3},
    {"category": "Logical Reasoning", "question": "If FRIEND is coded as HUMJTK, how is CANDLE coded?",
     "options": ["EDRIRL", "DFOQNR", "DFSGSK", "DFSGKR"], "answer": 0},
    {"category": "Logical Reasoning", "question": "Complete the series: A, C, E, G, ?",
     "options": ["H", "I", "J", "K"], "answer": 1},
    {"category": "Logical Reasoning", "question": "Pointing to a photo, Ram said, 'She is the daughter of my grandfather's only son.' Who is she?",
     "options": ["Ram's mother", "Ram's sister", "Ram's aunt", "Ram's daughter"], "answer": 1},
    {"category": "Logical Reasoning", "question": "Which number should replace the question mark: 3, 9, 27, 81, ?",
     "options": ["162", "216", "243", "324"], "answer": 2},

    {"category": "English Language", "question": "Choose the correct synonym of 'Abundant':",
     "options": ["Scarce", "Plentiful", "Limited", "Rare"], "answer": 1},
    {"category": "English Language", "question": "Choose the correct antonym of 'Optimistic':",
     "options": ["Hopeful", "Positive", "Pessimistic", "Confident"], "answer": 2},
    {"category": "English Language", "question": "Identify the correctly spelled word:",
     "options": ["Recieve", "Receive", "Receeve", "Receve"], "answer": 1},
    {"category": "English Language", "question": "Fill in the blank: She ___ to the market every day.",
     "options": ["go", "goes", "going", "gone"], "answer": 1},
    {"category": "English Language", "question": "Choose the correctly punctuated sentence:",
     "options": ["Its a nice day.", "It's a nice day.", "Its' a nice day.", "It is a nice day"], "answer": 1},
]

CATEGORIES = sorted({q["category"] for q in QUESTION_BANK})
PASS_PERCENTAGE = 40
SECONDS_PER_QUESTION = 60

sessions = {}


def generate_exam(question_bank, category=None, num_questions=10):
    pool = [q for q in question_bank if category in (None, "All Categories", q["category"])]
    num_questions = min(num_questions, len(pool))
    return random.sample(pool, num_questions)


def score_exam(questions, answers):
    correct = 0
    review = []

    for i, question in enumerate(questions):
        selected = answers.get(str(i))
        is_correct = selected is not None and int(selected) == question["answer"]
        if is_correct:
            correct += 1
        review.append({
            "question": question["question"],
            "options": question["options"],
            "correct_index": question["answer"],
            "selected_index": int(selected) if selected is not None else None,
            "is_correct": is_correct,
        })

    total = len(questions)
    percentage = round((correct / total) * 100, 2) if total else 0.0
    return {
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "passed": percentage >= PASS_PERCENTAGE,
        "review": review,
    }


PAGE_STYLE = """
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f8; margin: 0; color: #1f2937; }
  header { background: #0f172a; color: #fff; padding: 1.25rem 2rem; }
  header h1 { margin: 0; font-size: 1.4rem; }
  .container { max-width: 720px; margin: 2rem auto; background: #fff; padding: 2rem; border-radius: 8px;
               box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
  label { display: block; margin-top: 1rem; font-weight: 600; }
  input[type=text], select { width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #cbd5e1;
                              border-radius: 4px; box-sizing: border-box; }
  button { margin-top: 1.5rem; background: #2563eb; color: #fff; border: none; padding: 0.7rem 1.5rem;
           border-radius: 4px; font-size: 1rem; cursor: pointer; }
  button:hover { background: #1d4ed8; }
  .question { margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e5e7eb; }
  .question p.text { font-weight: 600; }
  .options label { font-weight: normal; margin-top: 0.4rem; }
  #timer { position: sticky; top: 0; background: #fef3c7; padding: 0.6rem 1rem; border-radius: 4px;
           font-weight: 600; margin-bottom: 1rem; }
  .result-summary { text-align: center; }
  .result-summary .score { font-size: 2.5rem; font-weight: 700; }
  .passed { color: #16a34a; }
  .failed { color: #dc2626; }
  .review .correct { color: #16a34a; }
  .review .incorrect { color: #dc2626; }
</style>
"""


def render_page(title, body):
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>{html.escape(title)}</title>{PAGE_STYLE}</head>
<body>
<header><h1>Competitive Examination Portal</h1></header>
<div class="container">{body}</div>
</body>
</html>"""


def render_home():
    options = "\n".join(f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in CATEGORIES)
    body = f"""
<h2>Start a New Exam</h2>
<form method="post" action="/start">
  <label for="name">Candidate Name</label>
  <input type="text" id="name" name="name" required>

  <label for="category">Category</label>
  <select id="category" name="category">
    <option value="All Categories">All Categories</option>
    {options}
  </select>

  <label for="num_questions">Number of Questions</label>
  <select id="num_questions" name="num_questions">
    <option value="5">5</option>
    <option value="10" selected>10</option>
    <option value="15">15</option>
  </select>

  <button type="submit">Start Exam</button>
</form>
"""
    return render_page("Competitive Examination Portal", body)


def render_exam(session_id, exam):
    questions_html = []
    for i, q in enumerate(exam["questions"]):
        options_html = "\n".join(
            f'<label><input type="radio" name="q{i}" value="{j}"> {html.escape(opt)}</label><br>'
            for j, opt in enumerate(q["options"])
        )
        questions_html.append(f"""
<div class="question">
  <p class="text">{i + 1}. {html.escape(q['question'])}</p>
  <div class="options">{options_html}</div>
</div>
""")

    total_seconds = len(exam["questions"]) * SECONDS_PER_QUESTION
    body = f"""
<h2>Exam in progress: {html.escape(exam['category'])}</h2>
<div id="timer">Time remaining: <span id="time-left">--:--</span></div>
<form method="post" action="/submit" id="exam-form">
  <input type="hidden" name="session_id" value="{html.escape(session_id)}">
  {''.join(questions_html)}
  <button type="submit">Submit Exam</button>
</form>
<script>
  var remaining = {total_seconds};
  var display = document.getElementById("time-left");
  function tick() {{
    var m = Math.floor(remaining / 60);
    var s = remaining % 60;
    display.textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    if (remaining <= 0) {{
      document.getElementById("exam-form").submit();
      return;
    }}
    remaining -= 1;
    setTimeout(tick, 1000);
  }}
  tick();
</script>
"""
    return render_page("Exam in Progress", body)


def render_result(candidate_name, category, result):
    status_class = "passed" if result["passed"] else "failed"
    status_text = "PASSED" if result["passed"] else "FAILED"

    review_items = []
    for item in result["review"]:
        outcome_class = "correct" if item["is_correct"] else "incorrect"
        selected = (
            item["options"][item["selected_index"]]
            if item["selected_index"] is not None
            else "No answer selected"
        )
        correct = item["options"][item["correct_index"]]
        review_items.append(f"""
<div class="question review">
  <p class="text">{html.escape(item['question'])}</p>
  <p class="{outcome_class}">Your answer: {html.escape(selected)}</p>
  <p>Correct answer: {html.escape(correct)}</p>
</div>
""")

    body = f"""
<div class="result-summary">
  <h2>Exam Results for {html.escape(candidate_name)}</h2>
  <p>Category: {html.escape(category)}</p>
  <p class="score">{result['correct']} / {result['total']}</p>
  <p>Score: {result['percentage']}%</p>
  <p class="{status_class}">{status_text}</p>
</div>
<h3>Answer Review</h3>
{''.join(review_items)}
<a href="/">Take Another Exam</a>
"""
    return render_page("Exam Results", body)


class ExamRequestHandler(BaseHTTPRequestHandler):
    def _send_html(self, content, status=200):
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_form(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        return parse_qs(body)

    def _get_session_id(self):
        cookie_header = self.headers.get("Cookie")
        if not cookie_header:
            return None
        jar = cookies.SimpleCookie(cookie_header)
        if "session_id" in jar:
            return jar["session_id"].value
        return None

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._send_html(render_home())
            return

        if path == "/exam":
            session_id = self._get_session_id()
            exam = sessions.get(session_id)
            if exam is None:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return
            self._send_html(render_exam(session_id, exam))
            return

        self._send_html("<h1>404 Not Found</h1>", status=404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/start":
            form = self._read_form()
            name = form.get("name", ["Candidate"])[0].strip() or "Candidate"
            category = form.get("category", ["All Categories"])[0]
            num_questions = int(form.get("num_questions", ["10"])[0])

            questions = generate_exam(QUESTION_BANK, category=category, num_questions=num_questions)
            session_id = uuid.uuid4().hex
            sessions[session_id] = {"candidate_name": name, "category": category, "questions": questions}

            self.send_response(302)
            self.send_header("Location", "/exam")
            self.send_header("Set-Cookie", f"session_id={session_id}; Path=/")
            self.end_headers()
            return

        if path == "/submit":
            form = self._read_form()
            session_id = form.get("session_id", [None])[0]
            exam = sessions.pop(session_id, None)
            if exam is None:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return

            answers = {}
            for i in range(len(exam["questions"])):
                key = f"q{i}"
                if key in form:
                    answers[str(i)] = form[key][0]

            result = score_exam(exam["questions"], answers)
            self._send_html(render_result(exam["candidate_name"], exam["category"], result))
            return

        self._send_html("<h1>404 Not Found</h1>", status=404)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("0.0.0.0", port), ExamRequestHandler)
    print(f"Competitive Examination Portal running at http://localhost:{port}/")
    server.serve_forever()
