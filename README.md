# 🍽️ Food Delivery Website

A simple and functional food delivery web application built with **Flask**, **SQLAlchemy**, and **SQLite**. The platform allows users to browse a categorized menu, add items to a cart, register/login, place orders, and manage their profile.

## 🚀 Features

- User registration and login system
- Profile page for viewing personal orders
- Categorized food menu
- Cart system with quantity management
- Order placement functionality
- Responsive front-end using HTML, CSS, and JavaScript
- Image-based product display
- SQLite database for data persistence
- Structured with templates and static folders

## 🛠️ Technologies Used

- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Templating:** Jinja2
- **containerization** Docker
- **Others:** Python dotenv for environment variables

---

## 🐳 Run with Docker

### 1. Build the image
```bash
docker build -t food-delivery:latest .
```

### 2. Create the database
```bash
docker run --rm -it -v ${PWD}:/app food-delivery:latest python create_db.py
```

### 3. Run the container
```bash
docker run -it --rm -p 8000:8000 -v ${PWD}:/app food-delivery:latest
```

Now open your browser at 👉 [http://localhost:8000](http://localhost:8000)

---

## 🧑‍💻 Local Installation (without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/food-delivery-site.git
cd food-delivery-site
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
python create_db.py
```

### 5. Run the app
```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)