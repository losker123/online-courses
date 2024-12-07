from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://course_user:course_pass@course-db/course_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(120), nullable=False)

    def __init__(self, title, description, instructor):
        self.title = title
        self.description = description
        self.instructor = instructor
# from models import Course

# Routes
@app.route("/")
def index():
    return jsonify({"message": "Course Service is running"}), 200

@app.route("/courses", methods=["GET"])
def get_courses():
    """Fetch all courses."""
    courses = Course.query.all()
    data = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor
        }
        for c in courses
    ]
    return jsonify(data), 200

@app.route("/courses", methods=["POST"])
def create_course():
    """Create a new course."""
    data = request.get_json()
    if not data or "title" not in data or "description" not in data or "instructor" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_course = Course(
        title=data["title"],
        description=data["description"],
        instructor=data["instructor"]
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course created", "course": {
        "id": new_course.id,
        "title": new_course.title,
        "description": new_course.description,
        "instructor": new_course.instructor
    }}), 201

@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Update an existing course."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json()
    if "title" in data:
        course.title = data["title"]
    if "description" in data:
        course.description = data["description"]
    if "instructor" in data:
        course.instructor = data["instructor"]

    db.session.commit()
    return jsonify({"message": "Course updated", "course": {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor
    }}), 200

@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Delete a course by ID."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted"}), 200

if __name__ == "__main__":
    # Initialize database and run the app
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
