"""
Index route - redirects to login page.
"""
from flask import redirect, url_for
from . import auth_bp


@auth_bp.route('/')
def index():
    """Redirect root to login page."""
    return redirect(url_for('auth.login'))
