"""
Reset password routes.
"""
from . import auth_bp
from app.controllers.auth import ResetPasswordController


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Password reset request page."""
    return ResetPasswordController.reset_password_page()


@auth_bp.route('/reset-password/verify-otp', methods=['GET', 'POST'])
def reset_password_verify_otp():
    """Password reset OTP verification page."""
    return ResetPasswordController.reset_password_verify_otp_page()


@auth_bp.route('/reset-password/new-password', methods=['GET', 'POST'])
def reset_password_new_password():
    """New password entry page."""
    return ResetPasswordController.reset_password_new_password_page()
