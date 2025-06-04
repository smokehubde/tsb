import os
from flask import request, redirect, url_for, render_template, session

from db import create_app, db, Product

app = create_app()
ADMIN_HOST = os.getenv("ADMIN_HOST", "127.0.0.1")
ADMIN_PORT = int(os.getenv("ADMIN_PORT", "8000"))

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


def main():
    """Start the admin web app and optionally expose it as a Tor hidden service."""
    onion_service = None
    ctx = None
    if os.getenv("TOR_CONTROL_PORT"):
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
