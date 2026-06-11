import allure
import pytest

from helpers.config import SessionConfig
from lib.api_client import ApiClient
from lib.api_facade import APIFacade
from lib.models.deleting.deleting_request_model import DeletingRequestPost
from lib.models.registration.registration_request_model import RegistrationRequestPost


@pytest.fixture(scope="module")
def public_api():
    client = ApiClient(base_url=SessionConfig.base_url.rstrip("/"))
    return APIFacade(client)


@allure.feature("Account API")
@allure.story("Create and delete account")
@allure.title("API: create account → verify 201 → delete → verify 200")
@allure.description(
    "Smoke test for the account lifecycle via REST API.\n"
    "Creates a user with Faker-generated data via POST /api/createAccount, "
    "asserts responseCode 201, then deletes the same user via DELETE /api/deleteAccount "
    "and asserts responseCode 200."
)
def test_create_and_delete_account(public_api):
    user = RegistrationRequestPost()
    resp = public_api.RegistrationModule.create_user(dict_data=user)
    body = resp.json()
    assert body.get("responseCode") == 201, f"Registration failed: {body}"

    delete_data = DeletingRequestPost(email=str(user.email), password=user.password)
    resp = public_api.DeletingModule.delete_user(dict_data=delete_data)
    body = resp.json()
    assert body.get("responseCode") == 200, f"Deletion failed: {body}"
