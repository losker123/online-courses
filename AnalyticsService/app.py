from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://analytics_user:analytics_pass@analytics-db/analytics_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
# from models import Analytics

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

# Routes
@app.route("/")
def index():
    return jsonify({"message": "Analytics Service is running"}), 200

@app.route("/analytics", methods=["GET"])
def get_analytics():
    """Fetch all analytics records."""
    analytics = Analytics.query.all()
    data = [
        {
            "id": a.id,
            "user_id": a.user_id,
            "activity": a.activity,
            "timestamp": a.timestamp
        }
        for a in analytics
    ]
    return jsonify(data), 200

@app.route("/analytics", methods=["POST"])
def create_analytics():
    """Add a new analytics record."""
    data = request.get_json()
    if not data or "user_id" not in data or "activity" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_analytics = Analytics(
        user_id=data["user_id"],
        activity=data["activity"],
        timestamp=datetime.utcnow()
    )
    db.session.add(new_analytics)
    db.session.commit()
    return jsonify({"message": "Analytics record created", "record": {
        "id": new_analytics.id,
        "user_id": new_analytics.user_id,
        "activity": new_analytics.activity,
        "timestamp": new_analytics.timestamp
    }}), 201

@app.route("/analytics/<int:analytics_id>", methods=["DELETE"])
def delete_analytics(analytics_id):
    """Delete an analytics record by ID."""
    record = Analytics.query.get(analytics_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Analytics record deleted"}), 200

if __name__ == "__main__":
    # Initialize database and run the app
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
