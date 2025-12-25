"""
Authentication routes blueprint.
Handles all authentication-related URLs.
"""
from flask import Blueprint, redirect, url_for
from app.controllers.auth_controller import AuthController

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redirect root to login page."""
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    return AuthController.login_page()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    return AuthController.register_page()


@auth_bp.route('/logout')
def logout():
    """Logout action."""
    return AuthController.logout_action()


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page."""
    return AuthController.verify_otp_page()


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP."""
    return AuthController.resend_otp()


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Password reset request page."""
    return AuthController.reset_password_page()


@auth_bp.route('/reset-password/verify-otp', methods=['GET', 'POST'])
def reset_password_verify_otp():
    """Password reset OTP verification page."""
    return AuthController.reset_password_verify_otp_page()


@auth_bp.route('/reset-password/new-password', methods=['GET', 'POST'])
def reset_password_new_password():
    """New password entry page."""
    return AuthController.reset_password_new_password_page()
