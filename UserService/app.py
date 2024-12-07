from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import datetime

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_user:user_pass@user-db/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
# from models import User
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Routes
@app.route("/")
def index():
    return jsonify({"message": "User Service is running"}), 200

@app.route("/users", methods=["GET"])
def get_users():
    """Fetch all users."""
    users = User.query.all()
    data = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at
        }
        for u in users
    ]
    return jsonify(data), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Fetch a user by ID."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }), 200

@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_user = User(
        name=data["name"],
        email=data["email"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "user": {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "created_at": new_user.created_at
    }}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user information."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    return jsonify({"message": "User updated", "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }}), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user by ID."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    # Initialize database and run the app
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5004)
