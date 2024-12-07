from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://notify_user:notify_pass@notification-db/notification_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with actual email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with actual password

db = SQLAlchemy(app)
mail = Mail(app)

# Import models
# from models import Notification
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, message, sent_at):
        self.user_id = user_id
        self.message = message
        self.sent_at = sent_at

# Routes
@app.route("/")
def index():
    return jsonify({"message": "Notification Service is running"}), 200

@app.route("/notifications", methods=["GET"])
def get_notifications():
    """Fetch all notifications."""
    notifications = Notification.query.all()
    data = [
        {
            "id": n.id,
            "user_id": n.user_id,
            "message": n.message,
            "sent_at": n.sent_at
        }
        for n in notifications
    ]
    return jsonify(data), 200

@app.route("/notifications", methods=["POST"])
def create_notification():
    """Create a new notification and send it."""
    data = request.get_json()
    if not data or "user_id" not in data or "email" not in data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Save notification to the database
    new_notification = Notification(
        user_id=data["user_id"],
        message=data["message"],
        sent_at=datetime.utcnow()
    )
    db.session.add(new_notification)
    db.session.commit()

    # Send the notification email
    try:
        msg = Message(
            subject="New Notification",
            sender="your_email@gmail.com",
            recipients=[data["email"]],
            body=data["message"]
        )
        mail.send(msg)
        return jsonify({"message": "Notification sent", "notification": {
            "id": new_notification.id,
            "user_id": new_notification.user_id,
            "message": new_notification.message,
            "sent_at": new_notification.sent_at
        }}), 201
    except Exception as e:
        return jsonify({"error": "Failed to send email", "details": str(e)}), 500

@app.route("/notifications/<int:notification_id>", methods=["DELETE"])
def delete_notification(notification_id):
    """Delete a notification."""
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200

if __name__ == "__main__":
    # Initialize database and run the app
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5003)
