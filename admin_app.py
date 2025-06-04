import os
from flask import (
    request,
    redirect,
    url_for,
    render_template,
    session,
    render_template_string,
)

ADMIN_HOST = os.getenv("ADMIN_HOST", "127.0.0.1")
ADMIN_PORT = int(os.getenv("ADMIN_PORT", "8000"))
ENV_FILE = os.getenv("ENV_FILE", os.path.join(os.path.dirname(__file__), ".env"))


def load_env(path: str | None = None) -> None:
    """Load variables from a .env file into ``os.environ``.

    When a path is given or ``ENV_FILE`` is explicitly set, environment
    variables from that file override existing ones. Otherwise, values are only
    added if missing. This mirrors the behaviour in ``bot.load_env`` and allows
    tests to control the configuration reliably.
    """

    env_path = path or ENV_FILE
    if not os.path.exists(env_path):
        return

    override = path is not None or "ENV_FILE" in os.environ

    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                if override:
                    os.environ[key] = value
                else:
                    os.environ.setdefault(key, value)

from db import create_app, db, Product, ShippingCost

load_env()
app = create_app()


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
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapped


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form.get('username') == os.getenv('ADMIN_USER') and
                request.form.get('password') == os.getenv('ADMIN_PASS')):
            session['logged_in'] = True
            return redirect(url_for('product_list'))
        error = "Invalid credentials"
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        desc = request.form['description']
        db.session.add(Product(name=name, price=price, description=desc))
        db.session.commit()
        return redirect(url_for('product_list'))
    return render_template('add_product.html')


@app.route('/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit_product(pid):
    product = Product.query.get_or_404(pid)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        db.session.commit()
        return redirect(url_for('product_list'))
    return render_template('edit_product.html', p=product)


@app.route('/delete/<int:pid>')
@login_required
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))


@app.route('/shipping', methods=['GET', 'POST'])
@login_required
def shipping():
    """Manage shipping costs per country."""
    message = None
    if request.method == 'POST':
        country = request.form.get('country', '').strip()
        cost_val = request.form.get('cost', '').strip()
        if not country:
            message = 'Country required'
        else:
            try:
                cost = float(cost_val)
            except ValueError:
                message = 'Invalid cost'
            else:
                entry = ShippingCost.query.filter_by(country=country).first()
                if entry:
                    entry.cost = cost
                else:
                    db.session.add(ShippingCost(country=country, cost=cost))
                db.session.commit()
                message = 'Saved'
    costs = ShippingCost.query.order_by(ShippingCost.country).all()
    return render_template('shipping.html', costs=costs, message=message)


@app.route('/shipping/delete/<int:sid>')
@login_required
def delete_shipping(sid):
    entry = ShippingCost.query.get_or_404(sid)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('shipping'))


@app.route('/tor', methods=['GET', 'POST'])
@login_required
def tor_settings():
    """Display and update Tor control settings."""
    message = None
    enabled = os.getenv('ENABLE_TOR', '0') in {'1', 'true', 'yes'}
    host = os.getenv('TOR_CONTROL_HOST', '127.0.0.1')
    port = os.getenv('TOR_CONTROL_PORT', '9051')
    password = os.getenv('TOR_CONTROL_PASS', '')
    if request.method == 'POST':
        enabled = request.form.get('enabled') == 'on'
        host = request.form.get('host', '').strip()
        port_input = request.form.get('port', '').strip()
        password = request.form.get('password', '')
        if not host:
            message = 'Host required'
        else:
            try:
                port_val = int(port_input)
                if not 1 <= port_val <= 65535:
                    raise ValueError
            except ValueError:
                message = 'Invalid port'
            else:
                update_env_var('ENABLE_TOR', '1' if enabled else '0')
                update_env_var('TOR_CONTROL_HOST', host)
                update_env_var('TOR_CONTROL_PORT', str(port_val))
                update_env_var('TOR_CONTROL_PASS', password)
                port = str(port_val)
                message = 'Settings updated'
    return render_template_string('''
        {% if message %}<p>{{ message }}</p>{% endif %}
        <form method="post">
            <label>Enable Tor
                <input type="checkbox" name="enabled" {% if enabled %}checked{% endif %}>
            </label><br>
            <input name="host" value="{{ host }}" placeholder="Control Host">
            <input name="port" type="number" value="{{ port }}" placeholder="Control Port">
            <input name="password" type="text" value="{{ password }}" placeholder="Password">
            <button type="submit">Save</button>
        </form>
    ''', enabled=enabled, host=host, port=port, password=password, message=message)


def main():
    """Start the admin web app and optionally expose it as a Tor hidden service."""
    onion_service = None
    ctx = None
    if os.getenv("ENABLE_TOR", "0") in {"1", "true", "yes"}:
        try:
            from tor_service import hidden_service
            ctx = hidden_service(ADMIN_PORT)
            onion_service = ctx.__enter__()
            print(f"Tor hidden service available at http://{onion_service}")
        except Exception as exc:  # pragma: no cover - Tor optional in tests
            print(f"Failed to start Tor hidden service: {exc}")
            onion_service = None
            ctx = None

    try:
        app.run(host=ADMIN_HOST, port=ADMIN_PORT)
    finally:
        if onion_service is not None and ctx is not None:
            ctx.__exit__(None, None, None)


if __name__ == '__main__':
    main()
