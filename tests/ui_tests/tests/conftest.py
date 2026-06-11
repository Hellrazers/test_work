import logging

import allure
import pytest

from helpers.config import SessionConfig
from lib.api_client import ApiClient
from lib.api_facade import APIFacade
from lib.models.deleting.deleting_request_model import DeletingRequestPost
from lib.models.registration.registration_request_model import RegistrationRequestPost

logger = logging.getLogger("tests")


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "base_url": SessionConfig.base_url.rstrip("/"),
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="function")
def registered_user():
    client = ApiClient(base_url=SessionConfig.base_url.rstrip("/"))
    facade = APIFacade(client)

    user = RegistrationRequestPost()

    with allure.step(f"[API PRE-CONDITION] Register user: {user.email}"):
        resp = facade.RegistrationModule.create_user(dict_data=user)
        body = resp.json()
        logger.info(f"[REGISTER] responseCode={body.get('responseCode')} message={body.get('message')}")
        assert body.get("responseCode") == 201, (
            f"User registration failed: {body.get('message')} (code {body.get('responseCode')})"
        )

    yield user

    with allure.step(f"[API POST-CONDITION] Delete user: {user.email}"):
        delete_data = DeletingRequestPost(email=str(user.email), password=user.password)
        resp = facade.DeletingModule.delete_user(dict_data=delete_data)
        body = resp.json()
        logger.info(f"[DELETE] responseCode={body.get('responseCode')} message={body.get('message')}")
