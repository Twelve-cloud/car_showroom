from jauth.backends import TokenBackend
from jauth.tasks import send_mail_to_verify_account


def create_and_send_verification_link(link, email: str) -> None:
    link = f"{link}?token={TokenBackend.generate_token(type='access', user_id=email)}"
    send_mail_to_verify_account.delay(email, link)
