import allure
from requests import Session

from lib.models.registration.registration_request_model import RegistrationRequestPost


class ApiRegistration:
    def __init__(self, api):
        self.api: Session = api
        self.path = "/api/createAccount"

    def create_user(self, dict_data: RegistrationRequestPost):
        payload_dict = dict_data.to_dict(exclude_none=True)
        with allure.step(f'Creating user with {payload_dict}'):
            resp = self.api.post(self.path, data=payload_dict, clear_headers=True)
        return resp
