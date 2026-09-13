import unittest
import os
import sys
import json

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

import app
import database

class TestStudentTaskAPI(unittest.TestCase):
    def setUp(self):
        # Use an isolated test database
        database.DB_FILE = os.path.join(os.path.dirname(__file__), "test_database.db")
        if os.path.exists(database.DB_FILE):
            os.remove(database.DB_FILE)
        
        database.init_db()
        app.app.testing = True
        self.client = app.app.test_client()

    def tearDown(self):
        if os.path.exists(database.DB_FILE):
            try:
                os.remove(database.DB_FILE)
            except PermissionError:
                pass

    def test_01_home_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn("Backend API is running", data['message'])

    def test_02_get_empty_records(self):
        response = self.client.get('/api/records')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['records'], [])

    def test_03_create_record_success(self):
        payload = {
            "name": "Rahul Kumar",
            "roll_number": "BCA101",
            "task": "Complete Python Assignment",
            "category": "Assignment",
            "status": "Pending"
        }
        response = self.client.post('/api/records', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['record']['name'], "Rahul Kumar")
        self.assertEqual(data['record']['id'], 1)

    def test_04_create_record_validation_error(self):
        payload = {
            "name": "",
            "roll_number": "BCA101",
            "task": "Missing name field",
            "category": "Assignment"
        }
        response = self.client.post('/api/records', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_05_get_record_by_id(self):
        # Create record first
        database.add_record("Priya Sharma", "BCA102", "Project Documentation", "Project", "Pending")
        response = self.client.get('/api/records/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['record']['name'], "Priya Sharma")

    def test_06_get_non_existent_record(self):
        response = self.client.get('/api/records/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_07_update_record(self):
        rec = database.add_record("Amit", "CS105", "Database Setup", "Exam", "Pending")
        rec_id = rec['id']

        update_payload = {
            "name": "Amit Kumar",
            "roll_number": "CS105",
            "task": "Database Setup Completed",
            "category": "Exam",
            "status": "Completed"
        }
        response = self.client.put(f'/api/records/{rec_id}', data=json.dumps(update_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['record']['status'], "Completed")
        self.assertEqual(data['record']['name'], "Amit Kumar")

    def test_08_update_non_existent_record(self):
        update_payload = {
            "name": "Ghost",
            "roll_number": "000",
            "task": "Nothing",
            "category": "Other",
            "status": "Pending"
        }
        response = self.client.put('/api/records/999', data=json.dumps(update_payload), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_09_delete_record(self):
        rec = database.add_record("To Delete", "DEL01", "Temporary Task", "Other", "Pending")
        rec_id = rec['id']

        response = self.client.delete(f'/api/records/{rec_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        # Verify deletion
        get_resp = self.client.get(f'/api/records/{rec_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_10_delete_non_existent_record(self):
        response = self.client.delete('/api/records/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
