"""
Resend OTP controller for handling OTP resend requests.
"""
from flask import session, jsonify
from app.services.auth_service import AuthService


class ResendOTPController:
    """Controller for OTP resend action."""
    
    @staticmethod
    def resend_otp():
        """Handle OTP resend request."""
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'Session expired. Please register again.'}), 400
        
        if AuthService.resend_otp(user_id):
            return jsonify({'success': True, 'message': 'New OTP has been sent to your email!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to send OTP. Please try again.'}), 500
