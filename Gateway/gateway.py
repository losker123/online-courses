from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/course", methods=["GET", "POST", "DELETE"])
def course_service():
    """Proxy for CourseService."""
    if request.method == "GET":
        response = requests.get("http://course-service:5000/courses")
    elif request.method == "POST":
        response = requests.post("http://course-service:5000/courses", json=request.get_json())
    elif request.method == "DELETE":
        course_id = request.args.get('id')
        response = requests.delete(f"http://course-service:5000/courses/{course_id}")
    return jsonify(response.json()), response.status_code

@app.route("/user", methods=["GET", "POST", "DELETE"])
def user_service():
    """Proxy for UserService."""
    if request.method == "GET":
        response = requests.get("http://user-service:5004/users")
    elif request.method == "POST":
        response = requests.post("http://user-service:5004/users", json=request.get_json())
    elif request.method == "DELETE":
        user_id = request.args.get('id')
        response = requests.delete(f"http://user-service:5004/users/{user_id}")
    return jsonify(response.json()), response.status_code

@app.route("/enrollment", methods=["GET", "POST", "DELETE"])
def enrollment_service():
    """Proxy for EnrollmentService."""
    if request.method == "GET":
        response = requests.get("http://enrollment-service:5002/enrollments")
    elif request.method == "POST":
        response = requests.post("http://enrollment-service:5002/enrollments", json=request.get_json())
    elif request.method == "DELETE":
        enrollment_id = request.args.get('id')
        response = requests.delete(f"http://enrollment-service:5002/enrollments/{enrollment_id}")
    return jsonify(response.json()), response.status_code

@app.route("/notification", methods=["GET", "POST", "DELETE"])
def notification_service():
    """Proxy for NotificationService."""
    if request.method == "GET":
        response = requests.get("http://notification-service:5003/notifications")
    elif request.method == "POST":
        response = requests.post("http://notification-service:5003/notifications", json=request.get_json())
    elif request.method == "DELETE":
        notification_id = request.args.get('id')
        response = requests.delete(f"http://notification-service:5003/notifications/{notification_id}")
    return jsonify(response.json()), response.status_code

@app.route("/analytics", methods=["GET", "POST", "DELETE"])
def analytics_service():
    """Proxy for AnalyticsService."""
    if request.method == "GET":
        response = requests.get("http://analytics-service:5000/analytics")
    elif request.method == "POST":
        response = requests.post("http://analytics-service:5000/analytics", json=request.get_json())
    elif request.method == "DELETE":
        analytics_id = request.args.get('id')
        response = requests.delete(f"http://analytics-service:5000/analytics/{analytics_id}")
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

