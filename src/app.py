"""Flask web interface for managing warehouses."""

import math

from flask import Flask, abort, redirect, render_template, request, url_for

from varasto import Varasto

app = Flask(__name__)
warehouses = []


def _quantity(field):
    """Return a non-negative finite quantity from a form field."""
    try:
        quantity = float(request.form[field])
    except (KeyError, ValueError):
        return None

    if not math.isfinite(quantity) or quantity < 0:
        return None

    return quantity


def _error_response(message):
    """Render the warehouse page with a validation error."""
    return render_template(
        "index.html",
        warehouses=warehouses,
        error=message,
    ), 400


def _warehouse_stock(warehouse_id, action):
    """Return a warehouse stock for a valid warehouse and action."""
    if warehouse_id >= len(warehouses):
        abort(404)
    if action not in ("add", "remove"):
        abort(404)

    return warehouses[warehouse_id]["stock"]


@app.get("/")
def index():
    """List warehouses and provide forms for managing them."""
    return render_template("index.html", warehouses=warehouses)


@app.post("/warehouses")
def create_warehouse():
    """Create a warehouse with the submitted name and capacity."""
    name = request.form.get("name", "").strip()
    capacity = _quantity("capacity")
    if not name or capacity is None:
        return _error_response("Anna varastolle nimi ja kelvollinen tilavuus.")

    warehouses.append({"name": name, "stock": Varasto(capacity)})
    return redirect(url_for("index"))


@app.post("/warehouses/<int:warehouse_id>/<action>")
def update_warehouse(warehouse_id, action):
    """Add stock to or remove stock from a warehouse."""
    stock = _warehouse_stock(warehouse_id, action)
    quantity = _quantity("quantity")
    if quantity is None:
        return _error_response(
            "Anna kelvollinen, nollaa suurempi tai yhtä suuri määrä."
        )

    if action == "add":
        stock.lisaa_varastoon(quantity)
    else:
        stock.ota_varastosta(quantity)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
