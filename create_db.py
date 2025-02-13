from flask import Flask
from models import Product, db
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        with open('food.json') as f:
            food_data = json.load(f)

            for food_data in food_data:
                food = Product()

                db.session.add(food)

            db.session.commit()