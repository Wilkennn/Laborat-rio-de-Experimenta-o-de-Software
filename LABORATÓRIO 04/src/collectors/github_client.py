from __future__ import annotations
import time
from typing import Any, Dict, Optional
import requests
from requests import Response
from .rate_limit import RateLimiter
from ..config.config import Config

class GitHubClient:
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": self.config.user_agent,
        }
        if self.config.github_token:
            headers["Authorization"] = f"token {self.config.github_token}"
        self.session.headers.update(headers)
        self.limiter = RateLimiter(self.session)

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, retries: int = None, timeout: float = 30.0) -> Response:
        retries = self.config.max_retries if retries is None else retries
        last_exc: Optional[Exception] = None
        for attempt in range(retries + 1):
            try:
                self.limiter.wait_if_needed()
                resp = self.session.get(url, params=params, timeout=timeout)
                if resp.status_code == 200:
                    return resp
                if resp.status_code in (429, 403):
                    # Rate limit: aguarda baseado nos headers
                    self.limiter.handle_rate_limit(resp)
                    continue
                if 500 <= resp.status_code < 600:
                    time.sleep(self.config.retry_backoff ** attempt)
                    continue
                resp.raise_for_status()
                return resp
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                last_exc = e
                # backoff progressivo
                time.sleep(self.config.retry_backoff ** attempt)
                continue
        # Se chegou aqui, re-levanta última exceção ou erro
        if last_exc:
            raise last_exc
        return resp

    def get_paged(self, url: str, params: Optional[Dict[str, Any]] = None, per_page: int = 100, max_pages: Optional[int] = None):
        page = 1
        while True:
            q = dict(params or {})
            q.update({"per_page": per_page, "page": page})
            resp = self.get(url, q, timeout=45.0)
            try:
                data = resp.json()
            except Exception:
                # Corpo não-JSON (rede instável/proxy). Encerra paginação de forma segura.
                break
            if not data:
                break
            yield data
            page += 1
            if max_pages and page > max_pages:
                break
