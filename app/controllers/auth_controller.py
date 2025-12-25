"""
Authentication controller for handling authentication-related requests.
"""
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.services.auth_service import AuthService


class AuthController:
    """Controller for authentication pages and actions."""
    
    @staticmethod
    def login_page():
        """Handle login page GET and POST requests."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        if request.method == 'POST':
            identifier = request.form.get('loginIdentifier')
            password = request.form.get('password')
            
            user = AuthService.authenticate_user(identifier, password)
            
            if user:
                # Log in the user with Flask-Login
                login_user(user, remember=True)
                
                # Check if profile is completed
                if not user.profile_completed:
                    flash('Please complete your profile to continue.', 'info')
                    return redirect(url_for('main.complete_profile'))
                
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid email/username or password. Please ensure your account is verified.', 'error')
        
        return render_template('auth/login.html')
    
    @staticmethod
    def register_page():
        """Handle registration page GET and POST requests."""
        if request.method == 'POST':
            # Fix field mapping: form sends 'fullName' not 'username'
            username = request.form.get('fullName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            
            user, error = AuthService.register_user(username, email, phone, password)
            
            if user:
                # Store user_id in session for OTP verification
                session['user_id'] = user.id
                session['user_email'] = user.email
                
                flash('Registration successful! Please check your email for the OTP code.', 'success')
                return redirect(url_for('auth.verify_otp'))
            else:
                flash(error or 'Registration failed', 'error')
        
        return render_template('auth/register.html')
    
    @staticmethod
    def logout_action():
        """Handle logout action."""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
    
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
    
    @staticmethod
    def reset_password_page():
        """Handle password reset request page."""
        if request.method == 'POST':
            email = request.form.get('email')
            
            # Generate and send password reset OTP
            user = AuthService.generate_password_reset_otp(email)
            
            if user:
                # Store user info in session for OTP verification
                session['reset_user_id'] = user.id
                session['reset_email'] = user.email
                
                flash('A 6-digit OTP has been sent to your email address.', 'success')
                return redirect(url_for('auth.reset_password_verify_otp'))
            else:
                flash('No account found with that email address.', 'error')
        
        return render_template('auth/reset-password.html')
    
    @staticmethod
    def reset_password_verify_otp_page():
        """Handle password reset OTP verification page."""
        if request.method == 'POST':
            otp = request.form.get('otp')
            
            # Get user_id from session
            user_id = session.get('reset_user_id')
            
            if not user_id:
                flash('Session expired. Please start the password reset process again.', 'error')
                return redirect(url_for('auth.reset_password'))
            
            # Use verify_password_reset_otp to avoid changing is_verified status
            if AuthService.verify_password_reset_otp(user_id, otp):
                flash('OTP verified successfully! Please enter your new password.', 'success')
                return redirect(url_for('auth.reset_password_new_password'))
            else:
                flash('Invalid or expired OTP. Please try again.', 'error')
        
        return render_template('auth/reset-password-verify-otp.html')
    
    @staticmethod
    def reset_password_new_password_page():
        """Handle new password entry page."""
        if request.method == 'POST':
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Get user_id from session
            user_id = session.get('reset_user_id')
            
            if not user_id:
                flash('Session expired. Please start the password reset process again.', 'error')
                return redirect(url_for('auth.reset_password'))
            
            if new_password != confirm_password:
                flash('Passwords do not match', 'error')
            else:
                if AuthService.reset_password(user_id, new_password):
                    # Clear session data after successful password reset
                    session.pop('reset_user_id', None)
                    session.pop('reset_email', None)
                    
                    flash('Password reset successful! Please log in with your new password.', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Password reset failed. Please try again.', 'error')
        
        return render_template('auth/reset-password-new-password.html')
