from flask import Flask, render_template
from models import Product

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route('/menu/')
def menu():
    return render_template('menu.html')


@app.route('/category/<string:category_name>/')
def category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    return render_template('category.html', products=products)


@app.route('/profile/')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)