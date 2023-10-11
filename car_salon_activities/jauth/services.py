from jauth.tasks import send_mail_to_verify_account
from jauth.models import User
from des import DesKey
from typing import Optional


DES_KEY = 'BrsblQfANOSaNKdEa6lZAmEh'


def send_verification_link(link: str, email: str) -> None:
    des_key = DesKey(DES_KEY.encode('utf-8'))
    encoded_email = des_key.encrypt(email.encode(), padding=True)
    link = f"{link}?token={encoded_email.decode()}"
    print(link)
    send_mail_to_verify_account.delay(email, link)


def confirm_email(user_token: str) -> Optional[User]:
    des_key = DesKey(DES_KEY.encode('utf-8'))
    email = des_key.decrypt(user_token.encode(), padding=True)
    print(email)
    user = User.objects.filter(email=email.decode()).first()

    if user is None:
        return None

    user.is_active = True
    user.save()
    return user
