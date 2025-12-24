"""
Authentication controller for handling authentication-related requests.
"""
from flask import render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService


class AuthController:
    """Controller for authentication pages and actions."""
    
    @staticmethod
    def login_page():
        """Handle login page GET and POST requests."""
        if request.method == 'POST':
            identifier = request.form.get('loginIdentifier')
            password = request.form.get('password')
            
            user = AuthService.authenticate_user(identifier, password)
            
            if user:
                # TODO: Implement proper session management with Flask-Login
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid email or password', 'error')
        
        return render_template('auth/login.html')
    
    @staticmethod
    def register_page():
        """Handle registration page GET and POST requests."""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            user, error = AuthService.register_user(username, email, password)
            
            if user:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash(error or 'Registration failed', 'error')
        
        return render_template('auth/register.html')
    
    @staticmethod
    def logout_action():
        """Handle logout action."""
        # TODO: Implement proper logout with Flask-Login
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
    
    @staticmethod
    def verify_otp_page():
        """Handle OTP verification page."""
        if request.method == 'POST':
            otp = request.form.get('otp')
            # TODO: Get user_id from session
            user_id = 1
            
            if AuthService.verify_otp(user_id, otp):
                flash('OTP verified successfully!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid OTP', 'error')
        
        return render_template('auth/verify-otp.html')
    
    @staticmethod
    def reset_password_page():
        """Handle password reset request page."""
        if request.method == 'POST':
            email = request.form.get('email')
            # TODO: Implement password reset email logic
            flash('Password reset instructions sent to your email.', 'info')
            return redirect(url_for('auth.reset_password_verify_otp'))
        
        return render_template('auth/reset-password.html')
    
    @staticmethod
    def reset_password_verify_otp_page():
        """Handle password reset OTP verification page."""
        if request.method == 'POST':
            otp = request.form.get('otp')
            
            if AuthService.verify_otp(1, otp):
                return redirect(url_for('auth.reset_password_new_password'))
            else:
                flash('Invalid OTP', 'error')
        
        return render_template('auth/reset-password-verify-otp.html')
    
    @staticmethod
    def reset_password_new_password_page():
        """Handle new password entry page."""
        if request.method == 'POST':
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('Passwords do not match', 'error')
            else:
                # TODO: Get user_id from session
                if AuthService.reset_password(1, new_password):
                    flash('Password reset successful! Please log in.', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Password reset failed', 'error')
        
        return render_template('auth/reset-password-new-password.html')
