import os
import secrets
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    orders = db.relationship('SnackOrder', backref='user', lazy=True)

class SnackProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.String(500))
    image_url = db.Column(db.String(200))

class SnackOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('snack_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('snack_product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('SnackProduct')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    featured_products = SnackProduct.query.limit(3).all()
    return render_template('index.html', featured_products=featured_products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash('Invalid credentials!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.route('/products')
def products():
    all_products = SnackProduct.query.all()
    return render_template('products.html', products=all_products)

@app.route('/products/<int:id>')
def product_detail(id):
    product = SnackProduct.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)

    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart

    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    cart = session.get('cart', {})
    for product_id, quantity in cart.items():
        product = SnackProduct.query.get(int(product_id))
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity

    user_balance = 0
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_balance = user.balance if user else 0

    return render_template('cart.html', cart_items=cart_items, total=total, user_balance=user_balance)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        if not cart:
            return redirect(url_for('cart'))

        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found!')
            return redirect(url_for('login'))

        total = 0
        for product_id, quantity in cart.items():
            product = SnackProduct.query.get(int(product_id))
            if product:
                total += product.price * quantity

        if user.balance < total:
            flash(f'Insufficient balance! You have ${user.balance:.2f} but need ${total:.2f}')
            return redirect(url_for('cart'))

        if total <= 0:
            flash('Total must be greater than zero!')
            return redirect(url_for('cart'))

        order = SnackOrder(user_id=session['user_id'], total=total)
        db.session.add(order)
        db.session.flush()

        for product_id, quantity in cart.items():
            product = SnackProduct.query.get(int(product_id))
            if product:
                item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)
                db.session.add(item)

        user.balance -= total

        db.session.commit()

        session.pop('cart', None)
        return redirect(url_for('order_confirmation', id=order.id))

    user = User.query.get(session['user_id'])
    return render_template('checkout.html', user_balance=user.balance if user else 0)

@app.route('/orders/<int:id>/receipt')
@login_required
def order_confirmation(id):
    order = SnackOrder.query.filter_by(id=id, user_id=session['user_id']).first_or_404()

    if any(item.product.name == 'Elite Hacker Snack' for item in order.items):
        return render_template('order_confirmation.html', order=order, flag=os.environ.get('FLAG', 'JCC25{lmao_flag}'))

    return render_template('order_confirmation.html', order=order)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/teapot')
def teapot():
    return render_template('teapot.html'), 418

def init_db():
    with app.app_context():
        db.create_all()

        products = [
            {
                'name': 'Stealth Cookies',
                'tagline': 'They disappear faster than your browser history.',
                'price': 4.20,
                'description': 'Dark chocolate cookies infused with mystery and intrigue.',
                'ingredients': '60% Dark Cocoa, 39% Flour, 1% Subterfuge',
                'image_url': '/static/stealth-cookies.png'
            },
            {
                'name': 'Proxy Puffs',
                'tagline': 'Bounce your cravings around the globe.',
                'price': 13.37,
                'description': 'Cheese puffs that route through multiple flavor profiles.',
                'ingredients': 'Cheddar, VPN Dust, International Spices',
                'image_url': '/static/proxy-puffs.png'
            },
            {
                'name': 'SQLi Sandwich',
                'tagline': 'DROP your hunger TABLE instantly!',
                'price': 8.08,
                'description': 'A sandwich that injects pure satisfaction into your taste buds.',
                'ingredients': 'SELECT * FROM delicious_ingredients',
                'image_url': '/static/sqli-sandwich.png'
            },
            {
                'name': 'BruteForce Brownies',
                'tagline': 'Guaranteed to crack your sweet tooth.',
                'price': 5.12,
                'description': 'Dense brownies that persistently attack your cravings.',
                'ingredients': '10000 attempts of chocolate, success guaranteed',
                'image_url': '/static/bruteforce-brownies.png'
            },
            {
                'name': 'Overflow Oreos',
                'tagline': 'Warning: bites may exceed buffer size.',
                'price': 3.14,
                'description': 'Extra-stuffed cookies that push the limits.',
                'ingredients': 'Cookie[2], Cream[99999], Buffer Overflow',
                'image_url': '/static/overflow-oreos.png'
            },
            {
                'name': 'Elite Hacker Snack',
                'tagline': 'Only for the 1337 - costs a fortune!',
                'price': 99999.99,
                'description': 'The ultimate snack that contains the flag. Can you afford it?',
                'ingredients': 'Pure digital gold, encrypted secrets, CTF flags',
                'image_url': '/static/elite-hacker-snack.png'
            }
        ]

        for p in products:
            product = SnackProduct(**p)
            db.session.add(product)

        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=4004, debug=False)
