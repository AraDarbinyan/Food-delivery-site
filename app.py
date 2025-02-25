from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Product, Customer, Cart, CartProduct, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fooddeliver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
login_meneger = LoginManager()
login_meneger.init_app(app)
login_meneger.login_message = 'view'

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route('/menu/')
def menu():
    return render_template('menu.html')


@app.route('/menu/category/<string:category_name>/')
def category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    return render_template('category.html', products=products)


@app.route('/cart/')
@login_required
def cart():
    cart = Cart.query.filter_by(customer_id=current_user.id).first()
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('menu'))
    
    cart_products = CartProduct.query.filter_by(cart_id=cart.id).all()
    return render_template('cart.html',  cart_products=cart_products)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(customer_id=current_user.id).first()
    if not cart:
        cart = Cart(customer_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if not cart_product:
        new_cart_product = CartProduct(cart_id=cart.id, product_id=product.id)
        db.session.add(new_cart_product)
    else:
        cart_product.quantity += 1
        
    db.session.commit()

    flash(f'{product.name} added to cart successfully!')
    return redirect(url_for('menu'))


@login_meneger.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Customer.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check your email and password')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Password does not match")
        return redirect(url_for('login'))
    

    hashed_password = generate_password_hash(password)
    new_user = Customer(name=name, email=email, phone=phone, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()


    flash('Account created successfully!')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', name=current_user.name, id=current_user.id)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)