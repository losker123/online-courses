import unittest
from unittest.mock import MagicMock
from flask import jsonify
from app import app, db, User

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and mock database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Using an in-memory database for simplicity
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app.testing = True

        # Mock the database session
        self.mock_db_session = MagicMock()
        db.session = self.mock_db_session

    def tearDown(self):
        """Clean up after each test."""
        # Reset mocks
        self.mock_db_session.reset_mock()

    def test_index(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Service is running', response.data)

    def test_get_users(self):
        """Test the GET /users route."""
        # Mock users data
        mock_users = [
            User(name="John Doe", email="john@example.com"),
            User(name="Jane Smith", email="jane@example.com")
        ]
        self.mock_db_session.query.return_value.all.return_value = mock_users

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['name'], "John Doe")
        self.assertEqual(users[1]['name'], "Jane Smith")

    def test_get_user(self):
        """Test the GET /users/<user_id> route."""
        # Mock a user
        mock_user = User(name="John Doe", email="john@example.com")
        mock_user.id = 1  # Ensure the mock user has an ID
        self.mock_db_session.query.return_value.get.return_value = mock_user

        response = self.app.get(f'/users/{mock_user.id}')
        self.assertEqual(response.status_code, 200)
        user_data = response.get_json()
        self.assertEqual(user_data['name'], "John Doe")
        self.assertEqual(user_data['email'], "john@example.com")

    def test_get_user_not_found(self):
        """Test GET /users/<user_id> when user is not found."""
        self.mock_db_session.query.return_value.get.return_value = None

        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_create_user(self):
        """Test the POST /users route."""
        new_user_data = {
            "name": "Alice", 
            "email": "alice@example.com"
        }
        mock_user = User(**new_user_data)
        mock_user.id = 2  # Assign an ID to the mock user
        self.mock_db_session.add.return_value = None
        self.mock_db_session.commit.return_value = None
        self.mock_db_session.refresh.return_value = None  # Simulate successful commit

        response = self.app.post('/users', json=new_user_data)
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
        # Mock a user
        mock_user = User(name="John Doe", email="john@example.com")
        mock_user.id = 1  # Ensure the mock user has an ID
        self.mock_db_session.query.return_value.get.return_value = mock_user

        updated_data = {
            "name": "John Updated", 
            "email": "johnupdated@example.com"
        }
        response = self.app.put(f'/users/{mock_user.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        updated_user = response.get_json()
        self.assertEqual(updated_user['user']['name'], "John Updated")
        self.assertEqual(updated_user['user']['email'], "johnupdated@example.com")

    def test_update_user_not_found(self):
        """Test PUT /users/<user_id> when user is not found."""
        self.mock_db_session.query.return_value.get.return_value = None

        response = self.app.put('/users/999', json={
            "name": "Nonexistent User", 
            "email": "nonexistent@example.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_delete_user(self):
        """Test the DELETE /users/<user_id> route."""
        mock_user = User(name="John Doe", email="john@example.com")
        mock_user.id = 1  # Ensure the mock user has an ID
        self.mock_db_session.query.return_value.get.return_value = mock_user
        self.mock_db_session.delete.return_value = None
        self.mock_db_session.commit.return_value = None

        response = self.app.delete(f'/users/{mock_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted', response.data)

    def test_delete_user_not_found(self):
        """Test DELETE /users/<user_id> when user is not found."""
        self.mock_db_session.query.return_value.get.return_value = None

        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

if __name__ == '__main__':
    unittest.main()
