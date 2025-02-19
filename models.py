from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model):

    __tablename__ = 'Customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return f'<Customer {self.name}>'


class Product(db.Model):

    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return f'<Product {self.name}>'
    

class Cart(db.Model):

    __tablename__ = 'Cart'

    id = db.Column(db.Integer, primary_key=True)
    customer_id =  db.Column(db.Integer, db.ForeignKey('Customer.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', secondary='cart_product', backref='carts')

    def __repr__(self):
        return f"<Cart {self.id} for Customer {self.customer_id}>"


cart_product = db.Table(
    'cart_product',
    db.Column('cart_id', db.Integer, db.ForeignKey('Cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('Product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1) 
)



class Order(db.Model):

    __tablename__ = 'Order'

    id = db.Column(db.Integer, primary_key=True)
    customer_id =  db.Column(db.Integer, db.ForeignKey('Customer.id'), nullable=False)
    total_price = db.Column(db.Numeric(8,2), nullable=False)
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'delivered', 'canceled', name="order_status"), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Order {self.id} for Customer {self.customer_id}>"
