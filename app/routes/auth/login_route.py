"""
Login route.
"""
from . import auth_bp
from app.controllers.auth import LoginController


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    return LoginController.login_page()
