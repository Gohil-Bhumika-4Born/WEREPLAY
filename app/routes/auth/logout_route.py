"""
Logout route.
"""
from . import auth_bp
from app.controllers.auth import LogoutController


@auth_bp.route('/logout')
def logout():
    """Logout action."""
    return LogoutController.logout_action()
