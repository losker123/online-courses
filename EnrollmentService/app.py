from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://enroll_user:enroll_pass@enroll-db/enroll_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
# from models import Enrollment
class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Float, nullable=False, default=0.0)  # Progress in percentage (0-100)
    enrolled_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, course_id, progress, enrolled_at):
        self.user_id = user_id
        self.course_id = course_id
        self.progress = progress
        self.enrolled_at = enrolled_at

# Routes
@app.route("/")
def index():
    return jsonify({"message": "Enrollment Service is running"}), 200

@app.route("/enrollments", methods=["GET"])
def get_enrollments():
    """Fetch all enrollments."""
    enrollments = Enrollment.query.all()
    data = [
        {
            "id": e.id,
            "user_id": e.user_id,
            "course_id": e.course_id,
            "progress": e.progress,
            "enrolled_at": e.enrolled_at
        }
        for e in enrollments
    ]
    return jsonify(data), 200

@app.route("/enrollments", methods=["POST"])
def create_enrollment():
    """Enroll a user in a course."""
    data = request.get_json()
    if not data or "user_id" not in data or "course_id" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_enrollment = Enrollment(
        user_id=data["user_id"],
        course_id=data["course_id"],
        progress=0,
        enrolled_at=datetime.utcnow()
    )
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({"message": "User enrolled", "enrollment": {
        "id": new_enrollment.id,
        "user_id": new_enrollment.user_id,
        "course_id": new_enrollment.course_id,
        "progress": new_enrollment.progress,
        "enrolled_at": new_enrollment.enrolled_at
    }}), 201

@app.route("/enrollments/<int:enrollment_id>", methods=["PUT"])
def update_progress(enrollment_id):
    """Update the progress of a user in a course."""
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    data = request.get_json()
    if "progress" not in data:
        return jsonify({"error": "Invalid data"}), 400

    enrollment.progress = data["progress"]
    db.session.commit()
    return jsonify({"message": "Progress updated", "enrollment": {
        "id": enrollment.id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "progress": enrollment.progress,
        "enrolled_at": enrollment.enrolled_at
    }}), 200

@app.route("/enrollments/<int:enrollment_id>", methods=["DELETE"])
def delete_enrollment(enrollment_id):
    """Delete an enrollment."""
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment deleted"}), 200

if __name__ == "__main__":
    # Initialize database and run the app
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5002)
