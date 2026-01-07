"""
Register route.
"""
from . import auth_bp
from app.controllers.auth import RegisterController


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    return RegisterController.register_page()
