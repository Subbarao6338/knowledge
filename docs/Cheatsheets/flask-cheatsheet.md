---
layout: default
title: "Flask Cheatsheet"
---

# Flask Cheatsheet

## 1. Quick Start & Minimal Application

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/api/status")
def get_status():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Runs the local development server on port 5000 with interactive debugger
    app.run(host="127.0.0.1", port=5000, debug=True)
```

---

## 2. Dynamic Routing & HTTP Methods

```python
from flask import request, abort, jsonify

@app.route("/user/<username>")
def show_user_profile(username):
    # Matches /user/jules
    return f"User profile: {username}"

@app.route("/post/<int:post_id>", methods=["GET", "PUT", "DELETE"])
def handle_post(post_id):
    if request.method == "GET":
        return f"Fetching post ID {post_id}"

    elif request.method == "PUT":
        data = request.get_json()
        return jsonify({"message": f"Updated post {post_id}", "payload": data}), 200

    elif request.method == "DELETE":
        return jsonify({"message": f"Deleted post {post_id}"}), 204
```

### URL Parameter Converters
- `<string:val>`: Accepts any text without a slash (default).
- `<int:val>`: Accepts integers.
- `<float:val>`: Accepts floating point numbers.
- `<path:val>`: Accepts strings with slashes (sub-paths).
- `<uuid:val>`: Accepts UUID strings.

---

## 3. Ingesting Client Request Data

```python
from flask import request, jsonify

@app.route("/submit", methods=["POST"])
def handle_submission():
    # 1. URL Query String Parameters: ?source=github&campaign=promo
    source = request.args.get("source", "unknown")

    # 2. JSON Request Payload: {"title": "New Bug", "priority": "High"}
    if request.is_json:
        data = request.get_json()
        title = data.get("title")
    else:
        # 3. Form Parameters (Standard URL-encoded form posts)
        title = request.form.get("title")

    # 4. Request Headers
    auth_header = request.headers.get("Authorization")

    # 5. File Upload
    uploaded_file = request.files.get("attachment")
    if uploaded_file:
        uploaded_file.save(f"/uploads/{uploaded_file.filename}")

    return jsonify({
        "status": "received",
        "source": source,
        "title": title
    }), 201
```

---

## 4. Context Globals & Thread Safety

Flask uses context-bound variables to access request details safely in multi-threaded environments.

| Context Object | Type | Description |
| :--- | :--- | :--- |
| `request` | Request Context | Accesses current HTTP request details (args, form, headers, JSON). |
| `session` | Request Context | Dict-like object for reading/writing cryptographically signed cookies. |
| `g` | Application Context | General namespace for temporary data shared during *one single* request lifetime. |
| `current_app` | Application Context | Points to the active Flask application instance currently serving the request thread. |

```python
from flask import g, session

# Session Setup requires a secure secret key to cryptographically sign session cookies
app.secret_key = "super-secret-key-change-in-production"

@app.before_request
def load_db_connection():
    # Store a database connection on g so it's accessible anywhere during this request
    g.db_conn = connect_to_database()

@app.teardown_request
def close_db_connection(exception):
    db_conn = getattr(g, "db_conn", None)
    if db_conn is not None:
        db_conn.close()
```

---

## 5. Modular Routes Configuration (Blueprints)

Blueprints allow you to organize routes and views into modular sub-sections of a large application.

### Creating a Blueprint (`auth.py`)
```python
from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"token": "signed-jwt-token-string"})

@auth_bp.route("/logout")
def logout():
    return jsonify({"message": "Successfully logged out"})
```

### Registering a Blueprint (`app.py`)
```python
from flask import Flask
from auth import auth_bp

app = Flask(__name__)

# Register the blueprint routes globally
app.register_blueprint(auth_bp)
```

---

## 6. Database Integration (Flask-SQLAlchemy)

### Model Definitions & Database Operations
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model Definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Create Database tables (run in CLI or initialization script)
with app.app_context():
    db.create_all()

# --- CRUD Operations ---

# Create
new_user = User(username="jules", email="jules@example.com")
db.session.add(new_user)
db.session.commit()

# Read
user = User.query.filter_by(username="jules").first()
all_users = User.query.all()

# Update
user.email = "jules.new@example.com"
db.session.commit()

# Delete
db.session.delete(user)
db.session.commit()
```

---

## 7. Unit Testing Flask Apps (pytest)

```python
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" # In-memory database

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

def test_json_api(client):
    response = client.post("/submit", json={"title": "Test Bug"})
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["title"] == "Test Bug"
```
