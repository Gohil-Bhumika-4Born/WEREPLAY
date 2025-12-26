"""
Login controller for handling login-related requests.
"""
from flask import render_template, request, redirect, url_for, flash
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
