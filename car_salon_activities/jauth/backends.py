from datetime import datetime, timedelta
from django.conf import settings
from typing import Optional
import jwt


class TokenBackend:
    @classmethod
    def generate_token(cls, *, type: str, user_id: int) -> str:
        match type:
            case 'access':
                lifetime = timedelta(
                    minutes=settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES']
                )
            case 'refresh':
                lifetime = timedelta(
                    days=settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS']
                )
            case _:
                raise ValueError('Unexpected type of token: must be access or refresh')

        expiry_token_date = datetime.now() + lifetime

        payload = {
            'sub': user_id,
            'exp': int(expiry_token_date.strftime('%s'))
        }

        return jwt.encode(payload, settings.SECRET_KEY, settings.JWT_TOKEN['ENCODE_ALG'])

    @classmethod
    def get_payload_by_token(cls, *, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                settings.JWT_TOKEN['DECODE_ALGS']
            )
            return payload
        except jwt.ExpiredSignatureError as expired:
            raise expired
        except jwt.PyJWTError:
            return None
