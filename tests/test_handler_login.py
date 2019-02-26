import mock
from flask import url_for

from redash.authentication.org_resolving import current_org
from tests import BaseTestCase


class TestLogin(BaseTestCase):
    @mock.patch('redash.settings.REMOTE_USER_LOGIN_ENABLED', return_value=True)
    def test_custom_login(self, remote_user_login_enabled_mock):
        """Test to make sure requests to /login are directed to the
        remote auth URL"""
        response = self.get_request('/login', org=self.factory.org)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location,
            url_for('remote_user_auth.login',
                next=url_for(
                    'redash.index',
                    org_slug=current_org.slug,
                    _external=False,
                ),
                org_slug=current_org.slug,
                _external=True,
            )
        )
