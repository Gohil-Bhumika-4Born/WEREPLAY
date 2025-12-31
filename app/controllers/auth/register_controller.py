"""
Register controller for handling registration-related requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from app.services.auth_service import AuthService


class RegisterController:
    """Controller for registration page and actions."""
    
    @staticmethod
    def register_page():
        """Handle registration page GET and POST requests."""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        # If registration already completed and waiting for OTP, redirect to OTP page
        if session.get('user_id') or session.get('registration_complete'):
            return redirect(url_for('auth.verify_otp'))

        errors = {}
        form_data = {}
        
        if request.method == 'POST':
            # Extract form data
            username = request.form.get('fullName', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirmPassword', '')
            
            # Store form data to retain values on error
            form_data = {
                'fullName': username,
                'email': email,
                'phone': phone
            }
            
            # Validate passwords match
            if password != confirm_password:
                errors['confirmPassword'] = 'Passwords do not match. Please try again.'
                return render_template('auth/register.html', errors=errors, form_data=form_data)
            
            user, error = AuthService.register_user(username, email, phone, password)
            
            if user:
                # Store user_id in session for OTP verification
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['registration_complete'] = True
                session['otp_verified'] = False
                
                flash('Registration successful! Please check your email for the OTP code.', 'success')
                return redirect(url_for('auth.verify_otp'))
            else:
                # Map service errors to field-specific errors
                if 'email' in error or 'Email' in error:
                    errors['email'] = error
                elif 'username' in error or 'Username' in error:
                    errors['fullName'] = error
                else:
                    errors['general'] = error or 'Registration failed. Please try again.'
                
                return render_template('auth/register.html', errors=errors, form_data=form_data)
        
        return render_template('auth/register.html', errors=errors, form_data=form_data)
