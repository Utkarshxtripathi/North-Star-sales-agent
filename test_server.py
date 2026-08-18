import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.tools import book_site_visit

# Unit test suite for API endpoints and booking tools
class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # Verify home page renders HTML template successfully
    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Northstar One", response.text)
        self.assertIn("CRM Lead Intelligence", response.text)

    # Verify health check endpoint returns 200 OK
    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["project"], "Northstar One (Sector 79, Gurugram)")

    # Verify empty chat input returns 400 Bad Request
    def test_chat_validation_error(self):
        response = self.client.post("/api/chat", json={"session_id": "test_sess_1", "message": "   "})
        self.assertEqual(response.status_code, 400)

    # Verify session reset clearing works correctly
    def test_session_reset(self):
        response = self.client.post("/api/session/reset", json={"session_id": "test_sess_1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    # Verify querying history on an uninitialized session returns empty list
    def test_session_history_empty(self):
        response = self.client.get("/api/session/non_existent_session/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["history"], [])

    # Verify booking tool executes successfully within visiting hours (3:00 PM)
    def test_tools_site_visit_success(self):
        result = book_site_visit(date="Tomorrow", time="3:00 PM", customer_name="Test User", configuration="2 BHK")
        self.assertEqual(result["status"], "success")
        self.assertTrue("NS1-" in result["booking_id"])
        self.assertEqual(result["date"], "Tomorrow")
        self.assertEqual(result["time"], "3:00 PM")

    # Verify booking tool rejects requests outside visiting hours (8:30 PM)
    def test_tools_site_visit_failure(self):
        result = book_site_visit(date="Today", time="8:30 PM")
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["error_code"], "SITE_CLOSED_AFTER_HOURS")
        self.assertIn("10:00 AM and 6:00 PM", result["reason"])
        self.assertTrue(len(result["suggested_slots"]) > 0)

if __name__ == "__main__":
    unittest.main()
