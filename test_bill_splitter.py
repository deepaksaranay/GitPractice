import pytest

from bill_splitter import (
    add_expense,
    add_member,
    calculate_balances,
    find_member,
    settle_up,
    split_amount,
    total_spent,
)


@pytest.fixture
def members():
    members = []
    for name in ["Alice", "Bob", "Cara"]:
        add_member(members, name)
    return members


def test_add_member_rejects_duplicates_case_insensitively(members):
    assert add_member(members, "alice") is False
    assert members == ["Alice", "Bob", "Cara"]


def test_find_member_is_case_insensitive(members):
    assert find_member(members, "bOB") == "Bob"
    assert find_member(members, "Dan") is None


def test_add_expense_defaults_to_everyone(members):
    expenses = []
    assert add_expense(expenses, members, "Pizza", 30, "alice") is True
    assert expenses[0] == {
        "description": "Pizza",
        "amount": 30,
        "paid_by": "Alice",
        "split_among": ["Alice", "Bob", "Cara"],
    }


def test_add_expense_rejects_unknown_member(members):
    expenses = []
    assert add_expense(expenses, members, "Taxi", 20, "Dan") is False
    assert add_expense(expenses, members, "Taxi", 20, "Alice", ["Bob", "Dan"]) is False
    assert expenses == []


def test_add_expense_rejects_non_positive_amount(members):
    expenses = []
    assert add_expense(expenses, members, "Nothing", 0, "Alice") is False
    assert add_expense(expenses, members, "Refund", -5, "Alice") is False


def test_split_amount_distributes_leftover_cents():
    assert split_amount(10, 3) == [3.34, 3.33, 3.33]
    assert sum(split_amount(10, 3)) == pytest.approx(10)


def test_calculate_balances(members):
    expenses = []
    add_expense(expenses, members, "Pizza", 30, "Alice")
    add_expense(expenses, members, "Taxi", 20, "Bob", ["Bob", "Cara"])
    assert calculate_balances(members, expenses) == {"Alice": 20, "Bob": 0, "Cara": -20}


def test_balances_always_sum_to_zero(members):
    expenses = []
    add_expense(expenses, members, "Snacks", 10, "Cara")
    add_expense(expenses, members, "Tickets", 47.35, "Bob", ["Alice", "Bob"])
    assert sum(calculate_balances(members, expenses).values()) == pytest.approx(0)


def test_calculate_balances_no_expenses(members):
    assert calculate_balances(members, []) == {"Alice": 0, "Bob": 0, "Cara": 0}


def test_settle_up(members):
    balances = {"Alice": 40, "Bob": -10, "Cara": -30}
    assert settle_up(balances) == [("Cara", "Alice", 30), ("Bob", "Alice", 10)]


def test_settle_up_zeroes_every_balance(members):
    expenses = []
    add_expense(expenses, members, "Dinner", 90.10, "Alice")
    add_expense(expenses, members, "Drinks", 25, "Bob", ["Bob", "Cara"])
    balances = calculate_balances(members, expenses)

    for debtor, creditor, amount in settle_up(balances):
        balances[debtor] += amount
        balances[creditor] -= amount

    assert all(balance == pytest.approx(0) for balance in balances.values())


def test_settle_up_nothing_owed():
    assert settle_up({"Alice": 0, "Bob": 0}) == []


def test_total_spent(members):
    expenses = []
    add_expense(expenses, members, "Pizza", 30, "Alice")
    add_expense(expenses, members, "Taxi", 12.5, "Bob")
    assert total_spent(expenses) == 42.5
