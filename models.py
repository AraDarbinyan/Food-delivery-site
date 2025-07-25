from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model, UserMixin):

    __tablename__ = 'Customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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
    ordered = db.Column(db.Boolean, default=False)

    cart_products = db.relationship('CartProduct', backref='cart', lazy=True)

    def __repr__(self):
        return f"<Cart {self.id} for Customer {self.customer_id}>"


class CartProduct(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    __table_args__ = (
        db.PrimaryKeyConstraint('cart_id', 'product_id'),
    )




class Order(db.Model):

    __tablename__ = 'Order'

    id = db.Column(db.Integer, primary_key=True)
    cart_id =  db.Column(db.Integer, db.ForeignKey('Cart.id'), nullable=False)
    total_price = db.Column(db.Numeric(8,2), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Order {self.id} of Customer {self.cart_id}>"
