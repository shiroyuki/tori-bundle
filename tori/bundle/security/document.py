from hashlib import md5
from tori.db.document import BaseDocument
from tori.db.document import document

class AccessPass(object):
    def __init__(self, id, name, alias, email, avatar_url=None):
        self._id    = id
        self._name  = name
        self._alias = alias
        self._email = email
        self._avatar_url = avatar_url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def alias(self):
        return self._alias

    @property
    def avatar_url(self):
        if not self._avatar_url:
            gravatar_id      = md5(self.email.lower()).hexdigest()
            self._avatar_url = 'http://www.gravatar.com/avatar/{}'.format(gravatar_id)

        return self._avatar_url

    def to_array(self):
        return {
            'id':    self._id,
            'name':  self._name,
            'alias': self._alias,
            'email': self._email
        }

@document('tori_security_provider')
class Provider(object):
    """Security Provider

    :param name: the name of the provider
    :type name:  str
    """
    def __init__(self, name, _id=None):
        self._id  = _id
        self.name = name

@document('tori_security_credential')
class Credential(BaseDocument):
    def __init__(self, email, hash, salt, provider, **attributes):
        '''
        Constructor

        :param email:      login credential
         :type email:      str
        :param hash:       password hash
         :type hash:       str
        :param salt:       password salt
         :type hash:       str
        :param provider:   authentication provider
         :type provider:   int
        :param attributes: the additional parameters
         :type attributes: dict
        :return:
        '''

        BaseDocument.__init__(self, **attributes)

        self.email    = email
        self.hash     = hash
        self.salt     = salt
        self.provider = provider

        if 'alias' not in attributes:
            self.alias = None
