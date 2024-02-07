# test_communication_bus.py

import unittest
import json
from communication_bus import app

class CommunicationBusTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_send_southbound_message(self):
        print("Testing sending a southbound message...")
        response = self.app.post('/southbound/aspirational_layer', data=json.dumps({'message': 'Test Message'}), content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json['status'])

    def test_receive_southbound_message(self):
        print("Testing receiving a southbound message...")
        self.app.post('/southbound/aspirational_layer', data=json.dumps({'message': 'Test Message'}), content_type='application/json')
        response = self.app.get('/receive/southbound/aspirational_layer')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Message', response.json['messages'])

    def test_send_northbound_message(self):
        print("Testing sending a northbound message...")
        response = self.app.post('/northbound/task_prosecution_layer', data=json.dumps({'message': 'Test Message'}), content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json['status'])

    def test_receive_northbound_message(self):
        print("Testing receiving a northbound message...")
        self.app.post('/northbound/task_prosecution_layer', data=json.dumps({'message': 'Test Message'}), content_type='application/json')
        response = self.app.get('/receive/northbound/task_prosecution_layer')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Message', response.json['messages'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
