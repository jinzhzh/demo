#!/usr/bin/env python3
"""
Unit tests for health_checker.py

Tests cover:
1. Successful HTTP response parsing and health determination
2. Timeout and retry logic with error handling
"""

import unittest
from unittest.mock import patch, MagicMock
from health_checker import HealthChecker, HealthCheckResult


class TestHealthCheckResult(unittest.TestCase):
    """Test the HealthCheckResult dataclass."""

    def test_to_dict(self):
        """Test that to_dict() produces a correct JSON-serializable dict."""
        result = HealthCheckResult(
            url="https://example.com",
            status_code=200,
            response_time_ms=150.5,
            is_healthy=True,
        )
        d = result.to_dict()
        self.assertEqual(d["url"], "https://example.com")
        self.assertEqual(d["status_code"], 200)
        self.assertEqual(d["response_time_ms"], 150.5)
        self.assertTrue(d["is_healthy"])
        self.assertIsNone(d["error"])

    def test_unhealthy_result(self):
        """Test that an unhealthy result is correctly represented."""
        result = HealthCheckResult(
            url="https://broken.example.com",
            status_code=None,
            response_time_ms=0.0,
            is_healthy=False,
            error="Connection refused",
        )
        d = result.to_dict()
        self.assertFalse(d["is_healthy"])
        self.assertEqual(d["error"], "Connection refused")


class TestHealthChecker(unittest.TestCase):
    """Test the HealthChecker class."""

    def setUp(self):
        """Set up a default HealthChecker for tests."""
        self.checker = HealthChecker(timeout=5.0, retries=2, max_concurrency=3)

    def test_initialization(self):
        """Test that HealthChecker initializes with correct defaults."""
        self.assertEqual(self.checker.timeout, 5.0)
        self.assertEqual(self.checker.retries, 2)
        self.assertEqual(self.checker.max_concurrency, 3)

    def test_invalid_timeout(self):
        """Test that negative timeout raises ValueError."""
        with self.assertRaises(ValueError):
            HealthChecker(timeout=-1)

    def test_invalid_retries(self):
        """Test that negative retries raises ValueError."""
        with self.assertRaises(ValueError):
            HealthChecker(retries=-1)

    def test_invalid_concurrency(self):
        """Test that zero concurrency raises ValueError."""
        with self.assertRaises(ValueError):
            HealthChecker(max_concurrency=0)

    @patch("health_checker.urllib.request.urlopen")
    def test_successful_request(self, mock_urlopen):
        """
        Test case 1: Successful HTTP response.

        Simulates a 200 OK response and verifies that:
        - status_code is correctly captured
        - is_healthy is True for 2xx responses
        - response_time_ms is a positive number
        """
        # Mock response object
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response

        result = self.checker.check_url("https://example.com/api/health")

        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.is_healthy)
        self.assertGreater(result.response_time_ms, 0)
        self.assertIsNone(result.error)

    @patch("health_checker.urllib.request.urlopen")
    def test_server_error_response(self, mock_urlopen):
        """
        Test case 2: Server error (5xx) response.

        Simulates a 503 Service Unavailable response and verifies that:
        - status_code is correctly captured
        - is_healthy is False for 5xx responses
        - The result is properly marked as unhealthy
        """
        # Mock HTTPError for 503
        mock_error = MagicMock()
        mock_error.code = 503
        mock_error.reason = "Service Unavailable"

        from urllib.error import HTTPError

        mock_urlopen.side_effect = HTTPError(
            url="https://broken-api.example.com",
            code=503,
            msg="Service Unavailable",
            hdrs={},
            fp=None,
        )

        result = self.checker.check_url("https://broken-api.example.com")

        self.assertEqual(result.status_code, 503)
        self.assertFalse(result.is_healthy)

    @patch("health_checker.urllib.request.urlopen")
    def test_timeout_with_retries(self, mock_urlopen):
        """
        Test timeout handling with retry logic.

        Simulates repeated TimeoutError exceptions and verifies that:
        - The checker retries the configured number of times
        - The final result is marked as unhealthy
        - The error message contains timeout information
        """
        import socket

        mock_urlopen.side_effect = socket.timeout("timed out")

        checker_with_retries = HealthChecker(timeout=1.0, retries=2)
        result = checker_with_retries.check_url("https://slow.example.com")

        # Should have been called 3 times (1 original + 2 retries)
        self.assertEqual(mock_urlopen.call_count, 3)
        self.assertFalse(result.is_healthy)
        self.assertIsNotNone(result.error)

    def test_check_urls_empty_list(self):
        """Test that an empty URL list returns an empty result list."""
        results = self.checker.check_urls([])
        self.assertEqual(results, [])

    @patch.object(HealthChecker, "check_url")
    def test_check_urls_concurrent(self, mock_check_url):
        """
        Test concurrent URL checking.

        Verifies that check_urls() dispatches all URLs and collects
        results in the correct order.
        """
        mock_check_url.side_effect = lambda url: HealthCheckResult(
            url=url,
            status_code=200,
            response_time_ms=100.0,
            is_healthy=True,
        )

        urls = [
            "https://api1.example.com",
            "https://api2.example.com",
            "https://api3.example.com",
        ]
        results = self.checker.check_urls(urls)

        self.assertEqual(len(results), 3)
        for i, r in enumerate(results):
            self.assertEqual(r.url, urls[i])
            self.assertTrue(r.is_healthy)


if __name__ == "__main__":
    unittest.main()
