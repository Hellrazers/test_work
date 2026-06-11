import allure
from requests import Session

from lib.models.deleting.deleting_request_model import DeletingRequestPost


class ApiDeleting:
    def __init__(self, api):
        self.api: Session = api
        self.path = "/api/deleteAccount"

    def delete_user(self, dict_data: DeletingRequestPost):
        payload_dict = dict_data.to_dict(exclude_none=True)
        with allure.step(f'Deleting user with {payload_dict}'):
            resp = self.api.delete(self.path, data=payload_dict, clear_headers=True)
        return resp
