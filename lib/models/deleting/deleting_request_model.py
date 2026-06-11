from faker import Faker
from pydantic import Field, EmailStr

from lib.models.base import BaseRequestSchema


def _fake() -> Faker:
    from helpers.config import SessionConfig
    return Faker(SessionConfig.faker_location or "en_US")


class DeletingRequestPost(BaseRequestSchema):
    email: EmailStr = Field(default_factory=lambda: _fake().email())
    password: str = "Password1234"
