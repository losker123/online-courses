import unittest
from flask import jsonify
from app import app, db, User

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and create a new database for each test."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app.testing = True

        # Bind the test database to the app context
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Service is running', response.data)

    def test_get_users(self):
        """Test the GET /users route."""
        # Create some users
        with app.app_context():
            user1 = User(name="John Doe", email="john@example.com")
            user2 = User(name="Jane Smith", email="jane@example.com")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['name'], "John Doe")
        self.assertEqual(users[1]['name'], "Jane Smith")

    def test_get_user(self):
        """Test the GET /users/<user_id> route."""
        # Create a user
        with app.app_context():
            user = User(name="John Doe", email="john@example.com")
            db.session.add(user)
            db.session.commit()

        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        user_data = response.get_json()
        self.assertEqual(user_data['name'], "John Doe")
        self.assertEqual(user_data['email'], "john@example.com")

    def test_get_user_not_found(self):
        """Test GET /users/<user_id> when user is not found."""
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_create_user(self):
        """Test the POST /users route."""
        response = self.app.post('/users', json={
            "name": "Alice", 
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)
        user_data = response.get_json()
        self.assertEqual(user_data['user']['name'], "Alice")
        self.assertEqual(user_data['user']['email'], "alice@example.com")

    def test_create_user_invalid_data(self):
        """Test POST /users with invalid data."""
        response = self.app.post('/users', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid data', response.data)

    def test_update_user(self):
        """Test the PUT /users/<user_id> route."""
        # Create a user
        with app.app_context():
            user = User(name="John Doe", email="john@example.com")
            db.session.add(user)
            db.session.commit()

        response = self.app.put(f'/users/{user.id}', json={
            "name": "John Updated", 
            "email": "johnupdated@example.com"
        })
        self.assertEqual(response.status_code, 200)
        updated_user = response.get_json()
        self.assertEqual(updated_user['user']['name'], "John Updated")
        self.assertEqual(updated_user['user']['email'], "johnupdated@example.com")

    def test_update_user_not_found(self):
        """Test PUT /users/<user_id> when user is not found."""
        response = self.app.put('/users/999', json={
            "name": "Nonexistent User", 
            "email": "nonexistent@example.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_delete_user(self):
        """Test the DELETE /users/<user_id> route."""
        # Create a user
        with app.app_context():
            user = User(name="John Doe", email="john@example.com")
            db.session.add(user)
            db.session.commit()

        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted', response.data)

    def test_delete_user_not_found(self):
        """Test DELETE /users/<user_id> when user is not found."""
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)


if __name__ == '__main__':
    unittest.main()
