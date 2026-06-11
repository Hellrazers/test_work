import logging

from lib.api_session import ApiSession

logger = logging.getLogger("tests")


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        logger.info("[API CLIENT] Initializing session")
        self.api = ApiSession(base_url=self.base_url)
