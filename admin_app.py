import os
from flask import request, redirect, url_for, render_template_string, session

from db import create_app, db, Product

app = create_app()
ADMIN_HOST = os.getenv("ADMIN_HOST", "127.0.0.1")
ADMIN_PORT = int(os.getenv("ADMIN_PORT", "8000"))
ENV_FILE = os.getenv("ENV_FILE", os.path.join(os.path.dirname(__file__), ".env"))


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
    return render_template_string('''
        {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
        <form method="post">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>''', error=error)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def product_list():
    products = Product.query.all()
    return render_template_string('''
        <a href="{{ url_for('add_product') }}">Neues Produkt</a>
        <ul>
        {% for p in products %}
            <li>
                {{ p.name }} - {{ p.price }} € - {{ p.description }}
                <a href="{{ url_for('edit_product', pid=p.id) }}">Edit</a>
                <a href="{{ url_for('delete_product', pid=p.id) }}">Delete</a>
            </li>
        {% endfor %}
        </ul>
    ''', products=products)


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
    return render_template_string('''
        <form method="post">
            <input name="name" placeholder="Name">
            <input name="price" placeholder="Price" type="number" step="0.01">
            <textarea name="description" placeholder="Beschreibung"></textarea>
            <button type="submit">Save</button>
        </form>
    ''')


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
    return render_template_string('''
        <form method="post">
            <input name="name" value="{{ p.name }}">
            <input name="price" type="number" step="0.01" value="{{ p.price }}">
            <textarea name="description">{{ p.description }}</textarea>
            <button type="submit">Save</button>
        </form>
    ''', p=product)


@app.route('/delete/<int:pid>')
@login_required
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))


@app.route('/tor', methods=['GET', 'POST'])
@login_required
def tor_settings():
    """Display and update Tor connection settings."""
    message = None
    host = os.getenv('TOR_HOST', '127.0.0.1')
    port = os.getenv('TOR_PORT', '9050')
    if request.method == 'POST':
        host = request.form.get('host', '').strip()
        port_input = request.form.get('port', '').strip()
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
                update_env_var('TOR_HOST', host)
                update_env_var('TOR_PORT', str(port_val))
                port = str(port_val)
                message = 'Settings updated'
    return render_template_string('''
        {% if message %}<p>{{ message }}</p>{% endif %}
        <form method="post">
            <input name="host" value="{{ host }}" placeholder="Host">
            <input name="port" type="number" value="{{ port }}" placeholder="Port">
            <button type="submit">Save</button>
        </form>
    ''', host=host, port=port, message=message)


def main():
    app.run(host=ADMIN_HOST, port=ADMIN_PORT)


if __name__ == '__main__':
    main()
