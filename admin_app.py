from flask import request, redirect, url_for, render_template_string, session
from db import create_app, db, Product

app = create_app()

ADMIN_USER = 'admin'
ADMIN_PASS = 'q12wq12w'


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
    if request.method == 'POST':
        if (request.form.get('username') == ADMIN_USER and
                request.form.get('password') == ADMIN_PASS):
            session['logged_in'] = True
            return redirect(url_for('product_list'))
    return render_template_string('''
        <form method="post">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>''')


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


def main():
    app.run(port=8000)


if __name__ == '__main__':
    main()
