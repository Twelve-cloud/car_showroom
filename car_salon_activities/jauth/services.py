from datetime import datetime, timedelta
from django.conf import settings
from typing import Optional
import jwt


def generate_token(*, type: str, user_id: int) -> str:
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


def get_payload_by_token(*, token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_TOKEN['DECODE_ALGS']
        )
        return payload
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        return None


def generate_token_pair(user_id: int) -> dict:
    access_token = generate_token(type='access',  user_id=user_id)
    refresh_token = generate_token(type='refresh',  user_id=user_id)
    return {'access': access_token, 'refresh': refresh_token}
