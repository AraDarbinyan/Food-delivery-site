from flask import Flask
from models import Product, db
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fooddeliver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        with open('food.json') as f:
            food_data = json.load(f)

            for food_data in food_data:
                food = Product(name=food_data['name'], category=food_data['category'], description=food_data['description'], price=food_data['price'], image_filename=food_data['image_filename'])

                db.session.add(food)

            db.session.commit()