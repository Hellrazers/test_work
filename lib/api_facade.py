from contract.deleting import ApiDeleting
from contract.registration import ApiRegistration


class APIFacade:
    def __init__(self, client):
        self.DeletingModule = ApiDeleting(client.api)
        self.RegistrationModule  = ApiRegistration(client.api)
