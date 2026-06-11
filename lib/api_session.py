import logging
import time
from urllib.parse import urlparse, urljoin

import allure
import requests
from requests import Session

from lib.allure_templates.allure_report_helper import add_attachment, MakoAttachmentRenderer, http_attachment

logger = logging.getLogger("tests")


class ApiSession(Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, data=None, headers=None, json=None, clear_headers=False, **kwargs):
        headers_data = {}
        if not clear_headers:
            headers_data["User-Agent"] = "node-superagent/3.8.3"
        if headers:
            headers_data.update(headers)

        url = self._build_url(url)

        parsed_url = urlparse(url)
        url_path = parsed_url.path + (f"?{parsed_url.query}" if parsed_url.query else "")
        logger.info(f"→ Method: {method}  Url path: {url_path}")
        if method.upper() not in ("GET", "DELETE"):
            payload = json if json is not None else data
            if payload:
                logger.info(f"  Payload: {payload}")

        start = time.perf_counter()
        with allure.step(f"{method} : {url}"):
            response = super().request(method=method, url=url, headers=headers_data, json=json, data=data, **kwargs)
        elapsed = round((time.perf_counter() - start) * 1000, 2)

        logger.info(f"← Status code: {response.status_code} Response time: {elapsed} ms")
        if response.status_code >= 400:
            try:
                logger.error(f"  ✗ Error response: {response.json()}")
            except Exception:
                logger.error(f"  ✗ Error response: {response.text[:500]}")

        self._add_attachments(response.request, response)
        return response

    @staticmethod
    def _add_attachments(request: requests.PreparedRequest, response: requests.Response):
        builder = http_attachment("Request")
        builder.add_url(request.url)
        builder.add_method(request.method)
        builder.add_headers(dict(request.headers))
        builder.add_body(request.body or "")
        add_attachment(builder.build(), MakoAttachmentRenderer("http_request.mak"))

        builder = http_attachment("Response")
        builder.add_response_code(response.status_code)
        builder.add_headers(dict(response.headers))
        builder.add_cookies(dict(response.cookies))
        builder.add_body(response.text or "")
        add_attachment(builder.build(), MakoAttachmentRenderer("http_response.mak"))

    def _build_url(self, path: str) -> str:
        return path if bool(urlparse(path).netloc) else urljoin(self.base_url, path)
