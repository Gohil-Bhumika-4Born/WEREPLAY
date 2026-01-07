"""
Verify OTP route.
"""
from . import auth_bp
from app.controllers.auth import VerifyOTPController


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page."""
    return VerifyOTPController.verify_otp_page()
