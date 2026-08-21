import pytest

from inventory_management import (
    add_item,
    delete_item,
    find_item,
    low_stock_items,
    total_inventory_value,
    update_quantity,
)


@pytest.fixture
def items():
    items = []
    add_item(items, "Widget", 10, 2.5)
    add_item(items, "Gadget", 3, 9.0)
    return items


def test_add_item(items):
    add_item(items, "Gizmo", 7, 5.0)
    assert find_item(items, "Gizmo") == {"name": "Gizmo", "quantity": 7, "price": 5.0}


def test_find_item_is_case_insensitive(items):
    assert find_item(items, "widget")["name"] == "Widget"


def test_find_item_not_found(items):
    assert find_item(items, "Missing") is None


def test_update_quantity(items):
    assert update_quantity(items, "Widget", 20) is True
    assert find_item(items, "Widget")["quantity"] == 20


def test_update_quantity_not_found(items):
    assert update_quantity(items, "Missing", 20) is False


def test_delete_item(items):
    assert delete_item(items, "Widget") is True
    assert find_item(items, "Widget") is None


def test_delete_item_not_found(items):
    assert delete_item(items, "Missing") is False


def test_total_inventory_value(items):
    assert total_inventory_value(items) == 10 * 2.5 + 3 * 9.0


def test_total_inventory_value_empty():
    assert total_inventory_value([]) == 0


def test_low_stock_items(items):
    low_stock = low_stock_items(items, threshold=5)
    assert [item["name"] for item in low_stock] == ["Gadget"]
