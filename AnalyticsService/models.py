from app import db

class Analytics(db.Model):
    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, activity, timestamp):
        self.user_id = user_id
        self.activity = activity
        self.timestamp = timestamp
