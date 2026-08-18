"""
Unit Tests for FastAPI Server Endpoints (Northstar One Sales Agent).
Tests health check, index route, chat endpoint validation, session resets, and tools.
"""

import unittest
from fastapi.testclient import TestClient
from main import app
from tools import book_site_visit


class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_index_route(self):
        """Verify that the home page renders HTML properly."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Northstar One", response.text)
        self.assertIn("CRM Lead Intelligence", response.text)

    def test_health_endpoint(self):
        """Verify that the health check endpoint returns 200 and healthy status."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["project"], "Northstar One (Sector 79, Gurugram)")

    def test_chat_validation_error(self):
        """Verify that empty chat messages return 400 Bad Request."""
        response = self.client.post("/api/chat", json={"session_id": "test_sess_1", "message": "   "})
        self.assertEqual(response.status_code, 400)

    def test_session_reset(self):
        """Verify that session reset endpoint works cleanly."""
        response = self.client.post("/api/session/reset", json={"session_id": "test_sess_1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_session_history_empty(self):
        """Verify that history for an empty session returns empty list."""
        response = self.client.get("/api/session/non_existent_session/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["history"], [])

    def test_tools_site_visit_success(self):
        """Unit test for tools.py: book_site_visit inside operating hours."""
        result = book_site_visit(date="Tomorrow", time="3:00 PM", customer_name="Test User", configuration="2 BHK")
        self.assertEqual(result["status"], "success")
        self.assertTrue("NS1-" in result["booking_id"])
        self.assertEqual(result["date"], "Tomorrow")
        self.assertEqual(result["time"], "3:00 PM")

    def test_tools_site_visit_failure(self):
        """Unit test for tools.py: book_site_visit outside operating hours (8:30 PM)."""
        result = book_site_visit(date="Today", time="8:30 PM")
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["error_code"], "SITE_CLOSED_AFTER_HOURS")
        self.assertIn("10:00 AM and 6:00 PM", result["reason"])
        self.assertTrue(len(result["suggested_slots"]) > 0)


if __name__ == "__main__":
    unittest.main()
