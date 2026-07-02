#!/usr/bin/env python3
"""
API Health Checker - Core Module

Provides the HealthChecker class for batch HTTP health checking with support
for timeout, retries, and concurrent requests.
"""

import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional


@dataclass
class HealthCheckResult:
    """Result of a single URL health check."""

    url: str
    status_code: Optional[int] = None
    response_time_ms: float = 0.0
    is_healthy: bool = False
    error: Optional[str] = None

    def to_dict(self):
        """Convert to a JSON-serializable dictionary."""
        return {
            "url": self.url,
            "status_code": self.status_code,
            "response_time_ms": round(self.response_time_ms, 2),
            "is_healthy": self.is_healthy,
            "error": self.error,
        }


class HealthChecker:
    """
    Batch HTTP health checker with timeout, retry, and concurrency support.

    Args:
        timeout: Request timeout in seconds (default: 10).
        retries: Number of retry attempts on failure (default: 0).
        max_concurrency: Maximum number of concurrent requests (default: 5).
    """

    def __init__(self, timeout: float = 10.0, retries: int = 0, max_concurrency: int = 5):
        if timeout <= 0:
            raise ValueError("Timeout must be a positive number")
        if retries < 0:
            raise ValueError("Retries cannot be negative")
        if max_concurrency < 1:
            raise ValueError("Max concurrency must be at least 1")

        self.timeout = timeout
        self.retries = retries
        self.max_concurrency = max_concurrency

    def check_url(self, url: str) -> HealthCheckResult:
        """
        Check a single URL's health status.

        Performs an HTTP GET request and measures response time.
        Retries on transient failures up to `self.retries` times.

        Args:
            url: The URL to check.

        Returns:
            HealthCheckResult with status code, response time, and health status.
        """
        last_error = None

        for attempt in range(1 + self.retries):
            result = self._do_request(url)
            if result.status_code is not None:
                return result
            last_error = result.error

            # Retry with exponential backoff
            if attempt < self.retries:
                backoff = min(2**attempt * 0.1, 2.0)
                time.sleep(backoff)

        # All retries exhausted
        return HealthCheckResult(
            url=url,
            status_code=None,
            response_time_ms=0.0,
            is_healthy=False,
            error=last_error or "Unknown error after all retries",
        )

    def _do_request(self, url: str) -> HealthCheckResult:
        """
        Perform a single HTTP GET request.

        Args:
            url: The URL to request.

        Returns:
            HealthCheckResult with the response details.
        """
        start_time = time.monotonic()

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "API-Health-Checker/1.0"},
                method="GET",
            )
            response = urllib.request.urlopen(req, timeout=self.timeout)
            elapsed_ms = (time.monotonic() - start_time) * 1000

            status_code = response.getcode()
            is_healthy = 200 <= status_code < 400

            return HealthCheckResult(
                url=url,
                status_code=status_code,
                response_time_ms=elapsed_ms,
                is_healthy=is_healthy,
            )

        except urllib.error.HTTPError as e:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            is_healthy = 200 <= e.code < 400
            return HealthCheckResult(
                url=url,
                status_code=e.code,
                response_time_ms=elapsed_ms,
                is_healthy=is_healthy,
            )

        except urllib.error.URLError as e:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            reason = str(e.reason)
            return HealthCheckResult(
                url=url,
                status_code=None,
                response_time_ms=elapsed_ms,
                is_healthy=False,
                error=f"URL Error: {reason}",
            )

        except TimeoutError:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return HealthCheckResult(
                url=url,
                status_code=None,
                response_time_ms=elapsed_ms,
                is_healthy=False,
                error=f"Timeout after {self.timeout}s",
            )

        except Exception as e:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return HealthCheckResult(
                url=url,
                status_code=None,
                response_time_ms=elapsed_ms,
                is_healthy=False,
                error=f"Unexpected error: {type(e).__name__}: {e}",
            )

    def check_urls(self, urls: List[str]) -> List[HealthCheckResult]:
        """
        Check multiple URLs concurrently.

        Uses a thread pool with bounded concurrency to check all URLs
        in parallel, returning results in the same order as input.

        Args:
            urls: List of URLs to check.

        Returns:
            List of HealthCheckResult objects, one per input URL.
        """
        if not urls:
            return []

        results = [None] * len(urls)

        with ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
            future_to_index = {
                executor.submit(self.check_url, url): idx
                for idx, url in enumerate(urls)
            }

            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = HealthCheckResult(
                        url=urls[idx],
                        status_code=None,
                        response_time_ms=0.0,
                        is_healthy=False,
                        error=f"Executor error: {e}",
                    )

        return results
