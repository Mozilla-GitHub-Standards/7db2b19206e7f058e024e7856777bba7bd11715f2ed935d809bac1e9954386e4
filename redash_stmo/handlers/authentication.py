from flask import redirect, request, url_for
from redash import settings
from redash.authentication import get_login_url, get_next_path
from redash.authentication.org_resolving import current_org


def extension(app):
    """An extension that automatically redirects from /login to /remote_user/login.
    """
    @app.before_request
    def redirect_login():
        login_path = get_login_url(external=False, next=None)
        if (settings.REMOTE_USER_LOGIN_ENABLED
                and not request.is_xhr
                and request.path.startswith(login_path)):
            org_slug = current_org.slug
            index_url = url_for('redash.index', org_slug=org_slug)
            unsafe_next_path = request.args.get('next', index_url)
            next_path = get_next_path(unsafe_next_path)
            return redirect(url_for('remote_user_auth.login', next=next_path, org_slug=org_slug))
