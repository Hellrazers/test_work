import inspect
from dataclasses import dataclass, field, asdict
from json import dumps, loads
from pathlib import Path

import allure
from mako.lookup import TemplateLookup

from helpers.common_helpers import not_none_or_empty, not_none


@dataclass
class Content:
    url: str = ""
    method: str = ""
    body: str = ""
    cookies: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    response_code: str = ""


@dataclass
class AttachmentData:
    name: str
    data: Content

class HttpAttachmentBuilder:

    def __init__(self, name: str):
        not_none_or_empty(name, "Name must not be none or empty value")
        self._name = name
        self._data = Content()

    def add_header(self, name: str, value: str):
        not_none_or_empty(name, "Header name must not be none or empty value")
        not_none_or_empty(value, "Header value must not be none or empty value")
        self._data.headers[name] = value

    def add_headers(self, headers: dict):
        not_none(headers, "Headers must not be none value")
        self._data.headers.update(headers)

    def add_cookie(self, name: str, value: str):
        not_none_or_empty(name, "Cookie name must not be none value")
        not_none_or_empty(value, "Cookie value must not be none value")
        self._data.cookies[name] = value

    def add_cookies(self, cookies: dict):
        not_none(cookies, "Cookies must not be none value")
        self._data.cookies.update(cookies)

    def add_body(self, body: str):
        not_none(body, "Body should not be none value")
        try:
            self._data.body = dumps(loads(body), indent=4)
        except Exception:
            self._data.body = body

    def add_url(self, url: str):
        self._data.url = not_none_or_empty(url, "Url must not be none or empty value")

    def add_method(self, method: str):
        self._data.method = not_none_or_empty(method, "Method must not be none or empty value")

    def add_response_code(self, value):
        self._data.response_code = not_none(value, "Url must not be none value")

    def build(self) -> AttachmentData:
        return AttachmentData(name=self._name, data=self._data)


def http_attachment(name: str) -> HttpAttachmentBuilder:
    return HttpAttachmentBuilder(name)


class MakoAttachmentRenderer:
    def __init__(self, template_name: str):
        self._template_name = template_name
        paths = Path(inspect.getfile(MakoAttachmentRenderer)).parent.absolute()
        self._template = TemplateLookup(directories=[paths]).get_template(template_name)

    def render(self, data: dict) -> str:
        return self._template.render(**data)


def add_attachment(attachment_data: AttachmentData, renderer: MakoAttachmentRenderer):
    content = renderer.render(asdict(attachment_data.data))
    allure.attach(body=content, name=attachment_data.name, attachment_type="text/html", extension=".html")
