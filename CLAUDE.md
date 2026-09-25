# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a personal Git/GitHub learning repository (`GitPractice`). It is not a single application — it's a
collection of small, independent, single-file Python CLI programs, each added in its own commit to practice
Git workflows. There is no shared package structure, build system, or linter configured anywhere in the repo.
Some scripts have accompanying `pytest` tests (see "Testing" below); there is otherwise nothing to build.

## Running the programs

Each `.py` file is a standalone, self-contained script with no external dependencies (standard library only,
Python 3). Run any of them directly:

```bash
python3 banking_system.py
python3 bill_splitter.py
python3 calculator.py
python3 contact_book.py
python3 expense_tracker.py
python3 hello.py
python3 library_management.py
python3 student_management.py
python3 todo.py
```

Most of these (`banking_system.py`, `bill_splitter.py`, `contact_book.py`, `expense_tracker.py`, `library_management.py`,
`student_management.py`, `todo.py`) are interactive, menu-driven console apps: they print a numbered menu in
a `while True` loop, read a choice via `input()`, and loop until the user selects the "Exit"/"Goodbye" option.
`calculator.py` prompts for two numbers and prints arithmetic results once, non-interactively. `hello.py` just
prints fixed lines.

There is no build step and no linter configured — there is nothing to run other than the scripts themselves
and their tests (see "Testing" below). Do not invent lint/build commands for this repo.

## Testing

A handful of scripts (e.g. `inventory_management.py`, `competitive_exam_portal.py`) have a matching
`test_<script>.py` file that imports their pure functions and tests them with `pytest`. Install the test
dependency and run the suite from the repo root:

```bash
pip install -r requirements-dev.txt
python3 -m pytest
```

`pytest.ini` pins the rootdir and test file pattern (`test_*.py`); no other configuration exists. When a
script is purely interactive with no extractable logic (e.g. `hello.py`, most menu-driven apps), it has no
tests — don't add a test file that just exercises `input()`/`print()` menu plumbing.

## Code conventions used across the scripts

These are the patterns consistently followed by the existing programs; match them when adding to an existing
file:

- In-memory state only: data lives in a module-level list or dict (`accounts = {}`, `tasks = []`, etc.) with
  no persistence to disk or a database — state resets every run.
- Menu loop shape: print a `===== Title =====` header and numbered options, read `choice = input(...)`, then
  branch with `if/elif` on the string choice, with a final `else: print("Invalid choice...")` and an `Exit`
  branch that `break`s out of the loop.
  - Record-style entities (contacts, books, expenses, students) are stored as dicts with named fields, e.g.
  `{"name": ..., "phone": ...}`.
- Lookups by name/title are done with a case-insensitive `.lower()` comparison in a linear scan (`for x in
  list: if x["field"].lower() == query.lower()`), often using `for...else` to detect a not-found case.
- Empty collections are checked explicitly (`if len(x) == 0` or `if not x`) with a friendly "No X found."
  message before attempting to iterate/print.

## Adding a new practice project

Follow the existing convention: one new top-level `.py` file per project, named after its domain
(`snake_case.py`), self-contained with no dependencies on the other files in the repo, and committed with a
message describing the addition (matching the existing history style, e.g. "Added \<Project Name\> project").
