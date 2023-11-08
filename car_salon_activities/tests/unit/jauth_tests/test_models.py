"""
test_models.py: File, containing tests for jauth.models.
"""


class TestUserModel:
    def test_get_username(self, user):
        assert user.get_username() == user.username

    def test_str(self, user):
        assert user.__str__() == user.username

    def test_is_anonymous(self, user):
        assert user.is_anonymous() is False

    def test_is_authenticated(self, user):
        assert user.is_authenticated() is True

    def test_set_password(self, user):
        old_password = user.password
        new_password = old_password + '_new'
        user.set_password(new_password)

        assert user.password != old_password
        assert user.check_password(new_password)

    def test_check_password(self, user):
        user_password = user.password
        user.set_password(user.password)

        assert user.check_password(user_password) is True

    def test_get_full_name(self, user):
        full_name = f'{user.first_name} {user.last_name}'.strip()

        assert user.get_full_name() == full_name

    def test_get_short_name(self, user):
        short_name = user.first_name.strip()

        assert user.get_short_name() == short_name

    def test_set_last_login(self, user):
        last_login = user.last_login
        user.set_last_login()

        assert user.last_login != last_login

    def test_set_active(self, user):
        user.is_active = False
        user.set_active()

        assert user.is_active is True
