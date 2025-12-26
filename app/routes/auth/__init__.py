"""
Authentication routes package.
"""
from flask import Blueprint

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Import all route modules to register them with the blueprint
from . import (
    index_route,
    login_route,
    register_route,
    logout_route,
    verify_otp_route,
    resend_otp_route,
    reset_password_route,
    complete_profile_route
)

__all__ = ['auth_bp']
