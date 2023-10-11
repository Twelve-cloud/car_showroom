"""
"""


from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from jauth.models import User


@shared_task
def send_mail_to_verify_account(email: str, link: str) -> None:
    send_mail(
        'Account Verification.',
        'Hello! You have registered at CarSA site.',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=(
            '<p><b>Click at the following link to verify account:</b></p>'
            f'<p><a href="{link}">Click to verify account</a></p>'
        )
    )


@shared_task
def clear_database_from_waste_accounts() -> None:
    User.objects.filter(is_active=False).delete()
