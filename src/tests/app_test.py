"""Tests for the Flask web interface."""

import app


def setup_function():
    """Reset application state before each test."""
    app.reset_warehouses()


def test_front_page_is_available():
    """The front page should be reachable."""
    client = app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Varastot".encode() in response.data


def test_warehouse_can_be_created_and_edited():
    """Warehouses should support create, add and remove operations."""
    client = app.app.test_client()

    create_response = client.post(
        "/create",
        data={"name": "KÄYTTÖ", "capacity": "10"},
    )
    assert create_response.status_code == 302
    assert client.post(
        "/warehouses/1/add",
        data={"amount": "4"},
    ).status_code == 302
    assert client.post(
        "/warehouses/1/remove",
        data={"amount": "1"},
    ).status_code == 302

    page = client.get("/")
    assert "KÄYTTÖ".encode() in page.data
    assert "3".encode() in page.data
