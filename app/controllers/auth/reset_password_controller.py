"""
Reset password controller for handling password reset requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from app.services.auth_service import AuthService


class ResetPasswordController:
    """Controller for password reset pages and actions."""
    
    @staticmethod
    def reset_password_page():
        """Handle password reset request page."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        # If password reset was just completed, redirect to login
        if session.get('password_reset_completed'):
            return redirect(url_for('auth.login', reset_success='true'))
        
        # If user already in password reset flow, redirect to next step
        if session.get('reset_otp_sent'):
            return redirect(url_for('auth.reset_password_verify_otp'))
        
        if request.method == 'POST':
            # Clear any previous password reset completion flag
            session.pop('password_reset_completed', None)
            
            email = request.form.get('email')
            
            # Generate and send password reset OTP
            user = AuthService.generate_password_reset_otp(email)
            
            if user:
                # Store user info in session for OTP verification
                session['reset_user_id'] = user.id
                session['reset_email'] = user.email
                session['reset_otp_sent'] = True
                session['reset_otp_verified'] = False
                
                flash('A 6-digit OTP has been sent to your email address.', 'success')
                return redirect(url_for('auth.reset_password_verify_otp'))
            else:
                flash('No account found with that email address.', 'error')
        
        return render_template('auth/reset-password.html')
    
    @staticmethod
    def reset_password_verify_otp_page():
        """Handle password reset OTP verification page."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        # If password reset was just completed, redirect to login
        if session.get('password_reset_completed'):
            return redirect(url_for('auth.login', reset_success='true'))
        
        # If OTP already verified, redirect to new password page
        if session.get('reset_otp_verified'):
            return redirect(url_for('auth.reset_password_new_password'))
        
        # If no reset session exists, redirect to start
        if not session.get('reset_user_id'):
            return redirect(url_for('auth.reset_password'))
        
        errors = {}
        
        # Get email from session for display
        email = session.get('reset_email', '')
        
        if request.method == 'POST':
            otp = request.form.get('otp')
            
            # Get user_id from session
            user_id = session.get('reset_user_id')
            
            if not user_id:
                errors['general'] = 'Session expired. Please start the password reset process again.'
                return render_template('auth/reset-password-verify-otp.html', errors=errors, email=email)
            
            # Use verify_password_reset_otp to avoid changing is_verified status
            if AuthService.verify_password_reset_otp(user_id, otp):
                # Set OTP verified flag
                session['reset_otp_verified'] = True
                
                flash('OTP verified successfully! Please enter your new password.', 'success')
                return redirect(url_for('auth.reset_password_new_password'))
            else:
                errors['otp'] = 'Invalid or expired OTP. Please check and try again.'
                return render_template('auth/reset-password-verify-otp.html', errors=errors, email=email)
        
        return render_template('auth/reset-password-verify-otp.html', errors=errors, email=email)
    
    @staticmethod
    def reset_password_new_password_page():
        """Handle new password entry page."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        # If password reset was just completed, redirect to login
        if session.get('password_reset_completed'):
            return redirect(url_for('auth.login', reset_success='true'))
        
        # If OTP not verified, redirect to OTP verification
        if not session.get('reset_otp_verified'):
            return redirect(url_for('auth.reset_password_verify_otp'))
        
        # If no reset session exists, redirect to start
        if not session.get('reset_user_id'):
            return redirect(url_for('auth.reset_password'))
        
        errors = {}
        
        if request.method == 'POST':
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Get user_id from session
            user_id = session.get('reset_user_id')
            
            if not user_id:
                errors['general'] = 'Session expired. Please start the password reset process again.'
                return render_template('auth/reset-password-new-password.html', errors=errors)
            
            if new_password != confirm_password:
                errors['confirmPassword'] = 'Passwords do not match. Please try again.'
                return render_template('auth/reset-password-new-password.html', errors=errors)
            
            if AuthService.reset_password(user_id, new_password):
                # Set completion flag BEFORE clearing other session data
                session['password_reset_completed'] = True
                
                # Clear all password reset session data
                session.pop('reset_user_id', None)
                session.pop('reset_email', None)
                session.pop('reset_otp_sent', None)
                session.pop('reset_otp_verified', None)
                
                # Redirect with success message as URL parameter
                return redirect(url_for('auth.login', reset_success='true'))
            else:
                errors['general'] = 'Password reset failed. Please try again.'
                return render_template('auth/reset-password-new-password.html', errors=errors)
        
        return render_template('auth/reset-password-new-password.html', errors=errors)
