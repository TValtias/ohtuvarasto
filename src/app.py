# pylint: disable=global-statement
"""Flask web interface for the warehouse application."""

from flask import Flask, redirect, render_template, request, url_for

try:
    from .varasto import Varasto
except ImportError:
    from varasto import Varasto


app = Flask(__name__, template_folder="../templates")

warehouses = {}
NEXT_WAREHOUSE_ID = 1


def reset_warehouses():
    """Clear the in-memory warehouses (used by tests)."""
    global NEXT_WAREHOUSE_ID
    warehouses.clear()
    NEXT_WAREHOUSE_ID = 1


@app.get("/")
def index():
    """Show all warehouses and the creation form."""
    return render_template("index.html", warehouses=warehouses)


@app.post("/create")
def create_warehouse():
    """Create a warehouse from the form."""
    global NEXT_WAREHOUSE_ID

    name = request.form.get("name", "").strip()
    try:
        capacity = float(request.form["capacity"])
    except (KeyError, ValueError):
        return redirect(url_for("index"))

    if name and capacity > 0:
        warehouse_id = NEXT_WAREHOUSE_ID
        NEXT_WAREHOUSE_ID += 1
        warehouses[warehouse_id] = {
            "name": name,
            "warehouse": Varasto(capacity),
        }

    return redirect(url_for("index"))


@app.post("/warehouses/<int:warehouse_id>/add")
def add_to_warehouse(warehouse_id):
    """Add goods to a warehouse."""
    item = warehouses.get(warehouse_id)
    if item is None:
        return redirect(url_for("index"))

    try:
        amount = float(request.form["amount"])
    except (KeyError, ValueError):
        return redirect(url_for("index"))

    if amount > 0:
        item["warehouse"].lisaa_varastoon(amount)

    return redirect(url_for("index"))


@app.post("/warehouses/<int:warehouse_id>/remove")
def remove_from_warehouse(warehouse_id):
    """Remove goods from a warehouse."""
    item = warehouses.get(warehouse_id)
    if item is None:
        return redirect(url_for("index"))

    try:
        amount = float(request.form["amount"])
    except (KeyError, ValueError):
        return redirect(url_for("index"))

    if amount > 0:
        item["warehouse"].ota_varastosta(amount)

    return redirect(url_for("index"))
