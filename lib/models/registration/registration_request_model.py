from typing import Optional
from uuid import uuid4
from faker import Faker
from pydantic import Field, EmailStr

from lib.models.base import BaseRequestSchema

AE_COUNTRIES = ["India", "United States", "Canada", "Australia", "Israel", "New Zealand", "Singapore"]


def _fake() -> Faker:
    from helpers.config import SessionConfig
    return Faker(SessionConfig.faker_location or "en_US")


class RegistrationRequestPost(BaseRequestSchema):
    name: str = Field(default_factory=lambda: _fake().name())
    email: EmailStr = Field(default_factory=lambda: f"user_{uuid4().hex[:12]}@{_fake().domain_name()}")
    password: str = "Password1234"
    title: str = Field(default_factory=lambda: _fake().random_element(elements=["Mr", "Mrs", "Miss"]))
    birth_date: int = Field(default_factory=lambda: _fake().random_int(min=1, max=28))
    birth_month: int = Field(default_factory=lambda: _fake().random_int(min=1, max=12))
    birth_year: int = Field(default_factory=lambda: _fake().random_int(min=1960, max=2005))
    firstname: str = Field(default_factory=lambda: _fake().first_name())
    lastname: str = Field(default_factory=lambda: _fake().last_name())
    company: str = Field(default_factory=lambda: _fake().company())
    address1: str = Field(default_factory=lambda: _fake().street_address())
    address2: Optional[str] = None
    country: str = Field(default_factory=lambda: _fake().random_element(elements=AE_COUNTRIES))
    zipcode: str = Field(default_factory=lambda: _fake().postcode())
    city: str = Field(default_factory=lambda: _fake().city())
    state: str = Field(default_factory=lambda: _fake().state())
    mobile_number: str = Field(default_factory=lambda: _fake().phone_number())
