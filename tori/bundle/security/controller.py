from tornado.auth    import GoogleMixin
from tornado.web     import asynchronous, HTTPError

from tori.bundle.common.handler     import Controller
from tori.bundle.security.document  import AccessPass
from tori.bundle.security.exception import ControllerException

class GoogleHandler(Controller, GoogleMixin):
    def get_provider_collection(self):
        pass

    @asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))

            return

        self.authenticate_redirect()

    def _on_auth(self, user):
        credentials = self.component('tori.collection.security.Credential')
        ''' :type credentials: tori.db.odm.collection.Collection '''

        providers = self.component('council.collection.security.Provider')
        ''' :type providers: tori.db.odm.collection.Collection '''

        if not user:
            self.redirect('/login/google/e403')

            return

        provider = providers.filter_one(name='Google')

        if not provider:
            raise ControllerException('The provider is not defined.')

        # Sample structure of "user"
        # --------------------------
        # {
        #   'first_name': 'Koichi',
        #   'claimed_id': 'https://www.google.com/accounts/o8/id?id=abcdef',
        #   'name':       'Koichi Nakayama',
        #   'locale':     'en',
        #   'last_name':  'Nakayama',
        #   'email':      'koichi@nakayama.jp'
        # }

        credential = self

        access_pass = AccessPass(credential.id, credential.name, credential.alias, credential.login)

        self.session.set('user', access_pass)

        self.redirect('/')