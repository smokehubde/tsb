# -*- coding: utf-8 -*-
"""Flask administration interface for the Telegram Shop Bot."""

from __future__ import annotations

import argparse
import logging
import os
from datetime import timedelta
from flask import (
    request,
    redirect,
    url_for,
    render_template,
    session,
    render_template_string,
)
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
from dotenv import load_dotenv


from config import load_env, setup_logging
from db import create_app, db, Product, ShippingCost

ADMIN_HOST = os.getenv("ADMIN_HOST", "0.0.0.0")
ADMIN_PORT = int(os.getenv("ADMIN_PORT", "8000"))
ENV_FILE = os.getenv("ENV_FILE", os.path.join(os.path.dirname(__file__), ".env"))


load_env()
app = create_app()
logger = logging.getLogger(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    minutes=int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
)
app.config["TESTING"] = os.getenv("FLASK_ENV") == "test"
if app.config["TESTING"]:
    app.config["WTF_CSRF_ENABLED"] = False

csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, enabled=not app.config["TESTING"])


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    app.logger.exception("Unhandled error: %s", error)
    return "Internal Server Error", 500


def update_env_var(name: str, value: str) -> None:
    """Persist a variable to the .env file and os.environ."""
    os.environ[name] = value
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{name}="):
            lines[i] = f"{name}={value}\n"
            found = True
            break
    if not found:
        lines.append(f"{name}={value}\n")
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)


def login_required(func):
    from functools import wraps

    @wraps(func)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapped


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        stored_hash = os.getenv("ADMIN_PASS_HASH")
        plain_pass = os.getenv("ADMIN_PASS")
        valid = False
        if username == os.getenv("ADMIN_USER"):
            if stored_hash:
                try:
                    valid = bcrypt.checkpw(password.encode(), stored_hash.encode())
                except ValueError:
                    valid = False
            elif plain_pass:
                valid = password == plain_pass
        if valid:
            session["logged_in"] = True
            session.permanent = True
            logger.info("Admin login from %s", request.remote_addr)
            return redirect(url_for("product_list"))
        logger.warning("Failed login from %s", request.remote_addr)
        error = "Invalid credentials"
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def product_list():
    products = Product.query.all()
    return render_template("product_list.html", products=products)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        desc = request.form["description"]
        db.session.add(Product(name=name, price=price, description=desc))
        db.session.commit()
        return redirect(url_for("product_list"))
    return render_template("add_product.html")


@app.route("/edit/<int:pid>", methods=["GET", "POST"])
@login_required
def edit_product(pid: int):
    product = Product.query.get_or_404(pid)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("product_list"))
    return render_template("edit_product.html", p=product)


@app.route("/delete/<int:pid>")
@login_required
def delete_product(pid: int):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("product_list"))


@app.route("/shipping", methods=["GET", "POST"])
@login_required
def shipping():
    """Manage shipping costs per country."""
    message = None
    if request.method == "POST":
        country = request.form.get("country", "").strip()
        cost_val = request.form.get("cost", "").strip()
        if not country:
            message = "Country required"
        else:
            try:
                cost = float(cost_val)
            except ValueError:
                message = "Invalid cost"
            else:
                entry = ShippingCost.query.filter_by(country=country).first()
                if entry:
                    entry.cost = cost
                else:
                    db.session.add(ShippingCost(country=country, cost=cost))
                db.session.commit()
                message = "Saved"
    costs = ShippingCost.query.order_by(ShippingCost.country).all()
    return render_template("shipping.html", costs=costs, message=message)


@app.route("/shipping/delete/<int:sid>")
@login_required
def delete_shipping(sid: int):
    entry = ShippingCost.query.get_or_404(sid)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("shipping"))


@app.route("/tor", methods=["GET", "POST"])
@login_required
def tor_settings():
    """Display and update Tor control settings."""
    message = None
    enabled = os.getenv("ENABLE_TOR", "0") in {"1", "true", "yes"}
    host = os.getenv("TOR_CONTROL_HOST", "127.0.0.1")
    port = os.getenv("TOR_CONTROL_PORT", "9051")
    password = os.getenv("TOR_CONTROL_PASS", "")
    if request.method == "POST":
        enabled = request.form.get("enabled") == "on"
        host = request.form.get("host", "").strip()
        port_input = request.form.get("port", "").strip()
        password = request.form.get("password", "")
        if not host:
            message = "Host required"
        else:
            try:
                port_val = int(port_input)
                if not 1 <= port_val <= 65535:
                    raise ValueError
            except ValueError:
                message = "Invalid port"
            else:
                update_env_var("ENABLE_TOR", "1" if enabled else "0")
                update_env_var("TOR_CONTROL_HOST", host)
                update_env_var("TOR_CONTROL_PORT", str(port_val))
                update_env_var("TOR_CONTROL_PASS", password)
                port = str(port_val)
                message = "Settings updated"
    return render_template_string(
        """
        {% if message %}<p>{{ message }}</p>{% endif %}
        <form method="post">

            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            {{ csrf_token() }}

            <label>Enable Tor
                <input type="checkbox" name="enabled" {% if enabled %}checked{% endif %}>
            </label><br>
            <input name="host" value="{{ host }}" placeholder="Control Host">
            <input name="port" type="number" value="{{ port }}" placeholder="Control Port">
            <input name="password" type="text" value="{{ password }}" placeholder="Password">
            <button type="submit">Save</button>
        </form>
        """,
        enabled=enabled,
        host=host,
        port=port,
        password=password,
        message=message,
    )


def main(argv: list[str] | None = None) -> None:
    """Start the admin web app and optionally expose a Tor hidden service."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    parser.add_argument("--host", default=ADMIN_HOST)
    parser.add_argument("--port", type=int, default=ADMIN_PORT)
    args = parser.parse_args(argv)
    setup_logging(getattr(logging, args.log_level.upper(), logging.INFO), "admin.log")
    onion_service = None
    ctx = None
    if os.getenv("ENABLE_TOR", "0") in {"1", "true", "yes"}:
        tor_dir = "/var/lib/tor/tsb_admin"
        try:
            if not os.path.exists(tor_dir):
                os.makedirs(tor_dir, mode=0o700, exist_ok=True)
            from tor_service import hidden_service

            ctx = hidden_service(args.port)
            onion_service = ctx.__enter__()
            logger.info("Tor hidden service available at http://%s", onion_service)
            onion_file = os.getenv(
                "ONION_FILE",
                os.path.join(os.path.dirname(__file__), "onion_url.txt"),
            )
            with open(onion_file, "w") as f:
                f.write(f"http://{onion_service}\n")
        except Exception as exc:  # pragma: no cover - Tor optional in tests
            logger.error("Failed to start Tor hidden service: %s", exc)
            onion_service = None
            ctx = None

    try:
        app.run(host=args.host, port=args.port)
    finally:
        if onion_service is not None and ctx is not None:
            ctx.__exit__(None, None, None)


if __name__ == "__main__":
    main()
