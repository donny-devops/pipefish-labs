import time
import unittest
from sdk.middleware import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    TokenBucketRateLimiter,
    ZeroRetentionRingBuffer
)

class TestMiddleware(unittest.TestCase):
    def test_circuit_breaker_success(self):
        cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=0.5)
        res = cb.call(lambda: "success")
        self.assertEqual(res, "success")
        self.assertEqual(cb.state, "CLOSED")

    def test_circuit_breaker_trips_to_open(self):
        cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=0.5)

        def faulty_call():
            raise ValueError("Upstream failure")

        # 1st failure
        with self.assertRaises(ValueError):
            cb.call(faulty_call)
        self.assertEqual(cb.state, "CLOSED")

        # 2nd failure -> trips to OPEN
        with self.assertRaises(ValueError):
            cb.call(faulty_call)
        self.assertEqual(cb.state, "OPEN")

        # Fast-fails with CircuitBreakerOpenError
        with self.assertRaises(CircuitBreakerOpenError):
            cb.call(lambda: "won't execute")

    def test_token_bucket_rate_limiter(self):
        limiter = TokenBucketRateLimiter(rate=10, capacity=2)
        self.assertTrue(limiter.acquire(1.0))
        self.assertTrue(limiter.acquire(1.0))
        # Now empty
        self.assertFalse(limiter.acquire(1.0))

    def test_zero_retention_ring_buffer(self):
        buf = ZeroRetentionRingBuffer(size=3)
        self.assertTrue(buf.push({"msg": "first"}))
        self.assertTrue(buf.push({"msg": "second"}))
        self.assertEqual(buf.count, 2)

        item1 = buf.pop()
        self.assertEqual(item1["msg"], "first")
        self.assertIsNone(buf.buffer[0])  # Overwritten with None/zeroed

        item2 = buf.pop()
        self.assertEqual(item2["msg"], "second")
        self.assertIsNone(buf.pop())  # Buffer empty

if __name__ == "__main__":
    unittest.main()
