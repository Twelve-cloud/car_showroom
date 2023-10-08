"""
"""


from jauth.backends import TokenBackend
from jauth.models import User


class Token:
    backend_class = TokenBackend

    def __init__(self, *, token, type):
        self.token = token
        self.type = type

    @classmethod
    def for_user(cls, user):
        access_token = cls.backend_class.generate_token(type='access', user_id=user.id)
        refresh_token = cls.backend_class.generate_token(type='refresh', user_id=user.id)
        return cls(token=access_token, type='access'), cls(token=refresh_token, type='refresh')

    def verify_token(self):
        pass

    def check_exp_date(self):
        pass

    def get_user_by_token(self):
        pass
