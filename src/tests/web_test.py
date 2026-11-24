"""Tests for the warehouse web interface."""

import unittest

from app import app, warehouses


class TestWeb(unittest.TestCase):
    """Tests the warehouse routes."""

    def setUp(self):
        """Create an isolated app client and warehouse list."""
        warehouses.clear()
        self.client = app.test_client()

    def test_create_and_list_warehouses(self):
        """Create multiple named warehouses and show them in the list."""
        response = self.client.post(
            "/warehouses",
            data={"name": "Mehu", "capacity": "10"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mehu", response.data)
        self.assertIn(b"Tilavuus: 10.0", response.data)

        self.client.post(
            "/warehouses",
            data={"name": "Olut", "capacity": "20"},
        )
        self.assertEqual(len(warehouses), 2)

    def test_add_and_remove_stock(self):
        """Add and remove stock through the web forms."""
        self.client.post("/warehouses", data={"name": "Mehu", "capacity": "10"})

        self.client.post("/warehouses/0/add", data={"quantity": "8"})
        response = self.client.post(
            "/warehouses/0/remove",
            data={"quantity": "3"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Saldo: 5.0", response.data)
        self.assertAlmostEqual(warehouses[0]["stock"].saldo, 5)

    def test_invalid_warehouse_data_is_rejected(self):
        """Reject a missing name and invalid capacity."""
        response = self.client.post(
            "/warehouses",
            data={"name": "", "capacity": "not a number"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please provide a name and a valid capacity", response.data)
        self.assertEqual(warehouses, [])

    def test_invalid_quantity_is_rejected(self):
        """Reject negative stock quantities without changing the balance."""
        self.client.post("/warehouses", data={"name": "Mehu", "capacity": "10"})

        response = self.client.post(
            "/warehouses/0/add",
            data={"quantity": "-1"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a valid quantity", response.data)
        self.assertEqual(warehouses[0]["stock"].saldo, 0)


if __name__ == "__main__":
    unittest.main()
