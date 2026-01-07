"""
Verify OTP controller for handling OTP verification requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user
from app.services.auth_service import AuthService


class VerifyOTPController:
    """Controller for OTP verification page."""
    
    @staticmethod
    def verify_otp_page():
        """Handle OTP verification page."""
        # Prevent access if user is already authenticated with complete profile
        if current_user.is_authenticated and current_user.profile_completed:
            return redirect(url_for('main.dashboard'))
        
        # If OTP already verified, redirect to profile completion
        if session.get('otp_verified'):
            return redirect(url_for('auth.complete_profile'))
        
        # If no registration session, redirect to register
        if not session.get('user_id'):
            return redirect(url_for('auth.register'))
        
        errors = {}
        
        # Get email from session for display
        email = session.get('user_email', '')
        
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
                
                # Set OTP verified flag before clearing user_id
                session['otp_verified'] = True
                
                # Clear registration session data after successful verification
                session.pop('user_id', None)
                session.pop('user_email', None)
                session.pop('registration_complete', None)
                
                # Log in the user
                login_user(user, remember=True)
                
                flash('Email verified successfully! Please complete your profile.', 'success')
                return redirect(url_for('auth.complete_profile'))
            else:
                errors['otp'] = 'Invalid or expired OTP. Please try again.'
                return render_template('auth/verify-otp.html', errors=errors, email=email)
        
        return render_template('auth/verify-otp.html', errors=errors, email=email)
