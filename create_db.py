from flask import Flask
from models import Product, db
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        with open('food.json') as f:
            food_data = json.load(f)

            for food_data in food_data:
                food = Product(name=food_data['name'], category=food_data['category'], description=food_data['description'], price=food_data['price'], image_path=food_data['image_path'])

                db.session.add(food)

            db.session.commit()