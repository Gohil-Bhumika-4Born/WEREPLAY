"""
Register controller for handling registration-related requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService


class RegisterController:
    """Controller for registration page and actions."""
    
    @staticmethod
    def register_page():
        """Handle registration page GET and POST requests."""
        if request.method == 'POST':
            # Fix field mapping: form sends 'fullName' not 'username'
            username = request.form.get('fullName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')
            
            # Validate passwords match
            if password != confirm_password:
                flash('Passwords do not match. Please try again.', 'error')
                return render_template('auth/register.html')
            
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
