from __future__ import annotations
import time
from typing import Optional
from requests import Response, Session

class RateLimiter:
    def __init__(self, session: Session, min_sleep: float = 1.0):
        self.session = session
        self.min_sleep = min_sleep

    def wait_if_needed(self) -> None:
        time.sleep(self.min_sleep)

    def handle_rate_limit(self, resp: Response) -> None:
        reset = resp.headers.get("X-RateLimit-Reset")
        if reset:
            try:
                reset_ts = int(reset)
                now = int(time.time())
                wait = max(0, reset_ts - now) + 1
                time.sleep(wait)
                return
            except Exception:
                pass
        # fallback
        time.sleep(60)
