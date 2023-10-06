from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.conf import settings
from user.models import User
from typing import Optional
import jwt


def generate_token(*, type: str, user_id: int) -> str:
    """
    generate_token: generates corresponding token for user.
    Parameters:
        1) type - type of the token. It can be 'access' or 'refresh'.
           If none of these types will be passed it raises an exception.
        2) user_id - user identifier. It's required because user_id is
           included by payload for authorization and authentication.
    """
    if type == 'access':
        lifetime = timedelta(
            minutes=settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES']
        )
    elif type == 'refresh':
        lifetime = timedelta(
            days=settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS']
        )
    else:
        raise ValueError('Unexpected type of token: must be access or refresh')

    expiry_token_date = datetime.now() + lifetime
    payload = {
        'sub': user_id,
        'exp': int(expiry_token_date.strftime('%s'))
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def set_tokens_to_cookie(response: Response, user_id: int) -> None:
    """
    set_token_to_cookie: set token to cookie to response object.
    """
    response.set_cookie(
        key='access_token',
        value=generate_token(type='access', user_id=user_id),
        secure=settings.JWT_TOKEN['SECURE'],
        httponly=settings.JWT_TOKEN['HTTP_ONLY']
    )

    response.set_cookie(
        key='refresh_token',
        value=generate_token(type='refresh', user_id=user_id),
        secure=settings.JWT_TOKEN['SECURE'],
        httponly=settings.JWT_TOKEN['HTTP_ONLY']
    )


def get_payload_by_token(token: str) -> Optional[dict]:
    """
    get_payload_by_token: returns payload of decoding token.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_TOKEN['ALGORITHMS']
        )
        return payload
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        return None


def verify_user(email: str) -> None:
    """
    verify_user: verify user if it exists, otherwise raise 404 error.
    """
    user = get_object_or_404(User, email=email)
    user.is_active = True
    user.save()