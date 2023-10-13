"""
tasks.py: File, containing celery tasks for a jauth application.
"""


from datetime import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from jauth.models import User


@shared_task
def send_verification_mail(email: str, verification_link: str) -> None:
    """
    send_verification_mail: Sends verification link to email address.

    Args:
        email (str): Email address.
        verification_link (str): Verification link (usually token).
    """

    send_mail(
        'Email Address Verification.',
        f'Verification link: {verification_link}',
        settings.EMAIL_HOST_USER,
        [email],
    )


@shared_task
def clear_database_from_waste_accounts() -> None:
    """
    clear_database_from_waste_accounts: Clears database from users that are inactive for one year.
    """

    User.objects.filter(
        is_active=False,
        last_login__lt=datetime.now() - relativedelta(years=1),
    ).delete()
