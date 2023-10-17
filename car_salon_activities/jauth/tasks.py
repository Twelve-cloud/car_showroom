"""
tasks.py: File, containing celery tasks for a jauth application.
"""


import logging
from datetime import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from jauth.models import User


logger = logging.getLogger(__name__)


@shared_task
def send_confirmation_mail(email: str, confirmation_link: str) -> None:
    """
    send_confirmation_mail: Sends confirmation link to email address.

    Args:
        email (str): Email address.
        confirmation_link (str): Confirmation link (usually token).
    """
    try:
        send_mail(
            'Email Address Confirmation.',
            f'Confirmation link: {confirmation_link}',
            settings.EMAIL_HOST_USER,
            [email],
        )
        logger.info(f'Mail to address {email} has been sent.')
    except Exception:
        logger.error(f'Mail to address {email} has not been sent.')


@shared_task
def clear_database_from_waste_accounts() -> None:
    """
    clear_database_from_waste_accounts: Clears database from users that are inactive for one year.
    """

    User.objects.filter(
        is_active=False,
        last_login__lt=datetime.now() - relativedelta(years=1),
    ).delete()
