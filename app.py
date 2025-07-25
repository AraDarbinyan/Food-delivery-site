from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Product, Customer, Cart, CartProduct, Order, db
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product


@app.route('/cart/')
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    cart = Cart.query.filter_by(customer_id=current_user.id, ordered=False).first()
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('menu'))
    
    cart_products = CartProduct.query.filter_by(cart_id=cart.id).all()
    return render_template('cart.html',  cart_products=cart_products, get_product=get_product)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        cart = Cart.query.filter_by(customer_id=current_user.id, ordered=False).first()
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

        
        return jsonify({"message": f"{product.name} added to cart successfully!"}), 200
    except AttributeError:
        return jsonify({"error": "You need to log in first"}), 401
    

@app.route('/update_cart/<int:product_id>/<action>', methods=['POST'])
@login_required
def update_cart(product_id, action):
    cart = Cart.query.filter_by(customer_id=current_user.id, ordered=False).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 400

    cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    if not cart_product:
        return jsonify({"error": "Product not found in cart"}), 400

    product = Product.query.get(cart_product.product_id) 


    if action == "increase":
        cart_product.quantity += 1
    elif action == "decrease":
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
    elif action == "remove":
        db.session.delete(cart_product)

    db.session.commit()

    total_price = sum(item.quantity * Product.query.get(item.product_id).price for item in cart.cart_products)

    return jsonify({
        "quantity": cart_product.quantity if action != "remove" else 0,
        "item_total_price": cart_product.quantity * product.price if action != "remove" else 0,  
        "total_price": total_price 
    })


@app.route('/order/', methods=['GET', 'POST'])
@login_required
def order():

    if request.method == 'POST':
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')

        cart = Cart.query.filter_by(customer_id=current_user.id, ordered=False).first()
        if cart:
            cart_products = CartProduct.query.filter_by(cart_id=cart.id)

        if  cart_products.count() == 0:
            flash("Your cart is empty") 
            return redirect(url_for('menu'))
        
        total_price = sum(item.quantity * Product.query.get(item.product_id).price for item in cart.cart_products)

        new_order = Order(
            cart_id=cart.id,
            total_price=total_price,
            payment_method=payment_method,
            delivery_address=address
        )
        db.session.add(new_order)
        db.session.commit()

        cart.ordered = True
        db.session.commit()

        flash("Ordered successfuly")
        return redirect(url_for('menu'))

    return render_template('order.html')


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
        customer = Customer.query.filter_by(id=current_user.id).first()
        past_carts = Cart.query.filter_by(customer_id=current_user.id, ordered=True).all()

        if not past_carts:
            flash("You have no past orders.", "info")
        orders = []

        for cart in past_carts:
            cart_products = CartProduct.query.filter_by(cart_id=cart.id).all()

            products = [{
                "name": Product.query.get(item.product_id).name,
                "quantity": item.quantity,
                "price": Product.query.get(item.product_id).price * item.quantity
            } for item in cart_products]

            order_details = {
                "id": cart.id,
                "created_at": cart.created_at.strftime('%Y-%m-%d %H:%M'),
                "total_price": sum(item["price"] for item in products),
                "products": products
            }

            orders.append(order_details)
        return render_template('profile.html', customer=customer, orders=orders)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)