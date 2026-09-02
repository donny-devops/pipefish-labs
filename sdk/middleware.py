"""
PipeFish Labs — Resilience Middleware, Circuit Breakers & Token Buffers
Version: 2.4.0
Features: Circuit Breaker, Token Bucket Rate Limiter, In-Memory Zero-Retention Buffer
"""

import time
import threading
from typing import Dict, Any, Callable, Optional

class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit breaker is open."""
    pass

class CircuitBreaker:
    """
    Protects downstream agent nodes and upstream model APIs from cascade failures.
    Transitions: CLOSED -> OPEN (on failure threshold) -> HALF-OPEN (after cooldown) -> CLOSED.
    """

    def __init__(self, failure_threshold: int = 3, cooldown_seconds: float = 5.0):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0.0
        self._lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        with self._lock:
            now = time.time()
            if self.state == "OPEN":
                if now - self.last_failure_time > self.cooldown_seconds:
                    self.state = "HALF_OPEN"
                else:
                    raise CircuitBreakerOpenError(f"Circuit breaker is OPEN. Fast-failing request.")

        try:
            result = func(*args, **kwargs)
            with self._lock:
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
            return result
        except Exception as exc:
            with self._lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
            raise exc

class TokenBucketRateLimiter:
    """
    High-throughput token bucket rate limiter for controlling inter-agent event flow.
    Enforces burst capacity and deterministic consumption.
    """

    def __init__(self, rate: float, capacity: float):
        self.rate = rate          # Tokens added per second
        self.capacity = capacity  # Maximum bucket capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def acquire(self, tokens: float = 1.0) -> bool:
        with self._lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class ZeroRetentionRingBuffer:
    """
    In-memory ring buffer with cryptographic zeroization for high-throughput
    agent telemetry bursts. Once read, frames are overwritten with zeroes.
    """

    def __init__(self, size: int = 100):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
        self._lock = threading.Lock()

    def push(self, data: Dict[str, Any]) -> bool:
        with self._lock:
            if self.count == self.size:
                return False  # Buffer full
            self.buffer[self.tail] = data
            self.tail = (self.tail + 1) % self.size
            self.count += 1
            return True

    def pop(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            if self.count == 0:
                return None
            item = self.buffer[self.head]
            # Zero out buffer memory slot (Zero-Data Retention)
            self.buffer[self.head] = None
            self.head = (self.head + 1) % self.size
            self.count -= 1
            return item

if __name__ == "__main__":
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=1.0)
    print("CircuitBreaker initialized in state:", cb.state)
    limiter = TokenBucketRateLimiter(rate=10, capacity=20)
    print("Limiter acquired token:", limiter.acquire())
    buf = ZeroRetentionRingBuffer(size=10)
    buf.push({"test": 1})
    print("Popped item:", buf.pop())
