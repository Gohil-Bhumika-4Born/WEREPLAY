"""
Verify OTP controller for handling OTP verification requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from app.services.auth_service import AuthService


class VerifyOTPController:
    """Controller for OTP verification page."""
    
    @staticmethod
    def verify_otp_page():
        """Handle OTP verification page."""
        if request.method == 'POST':
            otp = request.form.get('otp')
            
            # Get user_id from session
            user_id = session.get('user_id')
            
            if not user_id:
                flash('Session expired. Please register again.', 'error')
                return redirect(url_for('auth.register'))
            
            if AuthService.verify_otp(user_id, otp):
                # Get the user object
                from app.models.user import User
                user = User.query.get(user_id)
                
                # Clear session data after successful verification
                session.pop('user_id', None)
                session.pop('user_email', None)
                
                # Log in the user
                login_user(user, remember=True)
                
                flash('Email verified successfully! Please complete your profile.', 'success')
                return redirect(url_for('main.complete_profile'))
            else:
                flash('Invalid or expired OTP. Please try again.', 'error')
        
        return render_template('auth/verify-otp.html')
