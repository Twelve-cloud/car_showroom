from jauth.backends import TokenBackend
from jauth.models import User


class Token:
    backend_class = TokenBackend

    def __init__(self, refresh_token, access_token):
        self.refresh_token = refresh_token
        self.access_token = access_token

    @classmethod
    def for_user(cls, user):
        access_token = cls.backend_class.generate_token(type='access', user_id=user.id)
        refresh_token = cls.backend_class.generate_token(type='refresh', user_id=user.id)
        return cls(refresh_token, access_token)

    @classmethod
    def verify_token(cls, token):
        try:
            cls.backend_class.get_payload_by_token(token=token)
            return True
        except Exception:
            return False

    @classmethod
    def get_user_by_token(cls, token):
        payload = cls.backend_class.get_payload_by_token(token=token)

        if payload is None:
            return None

        user = User.objects.filter(id=payload['sub']).first()

        return user
