"""
Reset password controller for handling password reset requests.
"""
from flask import render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService


class ResetPasswordController:
    """Controller for password reset pages and actions."""
    
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
