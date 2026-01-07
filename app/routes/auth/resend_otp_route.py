"""
Resend OTP route.
"""
from . import auth_bp
from app.controllers.auth import ResendOTPController


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP."""
    return ResendOTPController.resend_otp()
