"""
test_tasks.py: File, containing tests for jauth.tasks.
"""


from jauth.tasks import send_confirmation_mail, clear_database_from_waste_accounts
from jauth.models import User


class TestJauthTasks:
    def test_send_confirmation_mail(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch('jauth.tasks.send_mail', mock)
        send_confirmation_mail('email', 'link')

        mock.assert_called_once()

        mock = mocker.MagicMock(side_effect=Exception)
        mocker.patch('jauth.tasks.send_mail', mock)
        send_confirmation_mail('email', 'link')

        mock.assert_called_once()

    def test_clear_database_from_waste_accounts(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(User.objects, 'filter', mock)
        clear_database_from_waste_accounts()

        mock.assert_called_once()
