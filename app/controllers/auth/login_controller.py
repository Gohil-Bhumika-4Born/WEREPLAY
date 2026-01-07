"""
Login controller for handling login-related requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user
from app.services.auth_service import AuthService


class LoginController:
    """Controller for login page and actions."""
    
    @staticmethod
    def login_page():
        """Handle login page GET and POST requests."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        # If registration in progress (OTP not yet verified), redirect to OTP page
        if session.get('user_id') and session.get('registration_complete') and not session.get('otp_verified'):
            return redirect(url_for('auth.verify_otp'))
        
        # If OTP verified but profile not completed, redirect to complete profile
        if session.get('otp_verified') and current_user.is_authenticated and not current_user.profile_completed:
            return redirect(url_for('auth.complete_profile'))
        
        errors = {}
        identifier = ''
        success_message = None
        
        # Check for password reset success
        if request.args.get('reset_success') == 'true':
            success_message = 'Password reset successful! Please log in with your new password.'
        
        if request.method == 'POST':
            identifier = request.form.get('loginIdentifier', '').strip()
            password = request.form.get('password', '')
            
            # Authenticate user - returns (user, error_code)
            user, error_code = AuthService.authenticate_user(identifier, password)
            
            if user:
                # Log in the user with Flask-Login
                login_user(user, remember=True)
                
                # Clear any residual registration/OTP session data
                session.pop('user_id', None)
                session.pop('user_email', None)
                session.pop('registration_complete', None)
                session.pop('otp_verified', None)
                
                # Clear any residual password reset session data
                session.pop('reset_user_id', None)
                session.pop('reset_email', None)
                session.pop('reset_otp_sent', None)
                session.pop('reset_otp_verified', None)
                session.pop('password_reset_completed', None)
                
                # Check if profile is completed
                if not user.profile_completed:
                    flash('Please complete your profile to continue.', 'info')
                    return redirect(url_for('auth.complete_profile'))
                
                # Successful login - redirect to dashboard
                flash('Login successful! Welcome back.', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                # Map error codes to field-specific inline errors
                if error_code == 'USER_NOT_FOUND':
                    errors['identifier'] = 'The email or username you entered is not registered. Please check and try again.'
                elif error_code == 'INVALID_PASSWORD':
                    errors['password'] = 'The password you entered is incorrect. Please try again or reset your password.'
                elif error_code == 'NOT_VERIFIED':
                    # Instead of showing error, redirect to OTP verification
                    # Get the user to set up session for OTP verification
                    from app.models.user import User
                    unverified_user = User.query.filter(
                        (User.email == identifier) | (User.username == identifier)
                    ).first()
                    
                    if unverified_user:
                        # Set up session for OTP verification
                        session['user_id'] = unverified_user.id
                        session['user_email'] = unverified_user.email
                        session['registration_complete'] = True
                        session['otp_verified'] = False
                        
                        flash('Your account is not verified. Please enter the OTP sent to your email.', 'info')
                        return redirect(url_for('auth.verify_otp'))
                    else:
                        errors['general'] = 'Account verification required.'
                else:
                    errors['general'] = 'Login failed. Please try again.'
                
                # Return template with identifier to retain form value and errors
                return render_template('auth/login.html', identifier=identifier, errors=errors, success_message=success_message)
        
        return render_template('auth/login.html', identifier=identifier, errors=errors, success_message=success_message)
