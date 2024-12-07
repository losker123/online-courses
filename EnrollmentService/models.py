from app import db

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
