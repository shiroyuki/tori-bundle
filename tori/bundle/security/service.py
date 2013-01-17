from tori.bundle.security.document import AccessPass
from tori.common import Enigma

class PasswordService(object):
    @staticmethod
    def generate(password, salt):
        return Enigma.instance().hash(password, salt)

class AuthenticationService(object):
    def __init__(self, credential_collection):
        self._credential_collection = credential_collection

    def register_credential(credential_information, provider=None):
        credential = self._credential_collection.filter_one(
            name       = credential_information['name'],
            login      = credential_information['email'],
            provider   = provider.id
        )

        if credential:
            return credential

        normalized_data = dict(credential_information)

        normalized_data.update({
            'hash':     None,
            'salt':     None,
            'provider': provider.id if provider else None
        })

        credential = credentials.new_document(**normalized_data)

        credentials.post(credential)

        return credential