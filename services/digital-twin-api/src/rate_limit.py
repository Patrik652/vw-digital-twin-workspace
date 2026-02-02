"""Simple token-bucket rate limiter."""

from __future__ import annotations

from dataclasses import dataclass, field
import time


@dataclass
class TokenBucket:
    capacity: int
    refill_per_sec: float
    tokens: float = field(init=False)
    last_refill: float = field(default_factory=time.monotonic)

    def __post_init__(self) -> None:
        self.tokens = float(self.capacity)

    def allow(self, amount: int = 1) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.last_refill = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_sec)
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False
