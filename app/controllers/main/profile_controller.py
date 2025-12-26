"""
Profile controller for handling profile-related requests.
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db


class ProfileController:
    """Controller for profile pages and actions."""
    
    @staticmethod
    @login_required
    def profile_page():
        """Render user profile page."""
        return render_template('main/profile.html', user=current_user)
    
    @staticmethod
    @login_required
    def profile_edit_page():
        """Handle profile edit page GET and POST requests."""
        if request.method == 'POST':
            try:
                # Update user profile with form data
                current_user.username = request.form.get('fullName')
                current_user.phone = request.form.get('phone')
                current_user.business_name = request.form.get('businessName')
                current_user.business_category = request.form.get('businessCategory')
                current_user.website_url = request.form.get('websiteUrl')
                current_user.country = request.form.get('country')
                current_user.state = request.form.get('state')
                current_user.city = request.form.get('city')
                current_user.pincode = request.form.get('pincode')
                current_user.timezone = request.form.get('timezone')
                current_user.preferred_language = request.form.get('preferredLanguage')
                current_user.notification_preference = request.form.get('notificationPreference')
                
                # Commit changes to database
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('main.profile'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating profile: {str(e)}', 'error')
                return render_template('main/profile-edit.html', user=current_user)
        
        return render_template('main/profile-edit.html', user=current_user)
    
    @staticmethod
    @login_required
    def profile_change_password_page():
        """Handle change password page GET and POST requests."""
        if request.method == 'POST':
            current_password = request.form.get('currentPassword')
            new_password = request.form.get('newPassword')
            confirm_password = request.form.get('confirmPassword')
            
            # Validate current password
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return render_template('main/profile-change-password.html')
            
            # Validate new passwords match
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return render_template('main/profile-change-password.html')
            
            # Validate new password is different from current
            if current_password == new_password:
                flash('New password must be different from current password', 'error')
                return render_template('main/profile-change-password.html')
            
            try:
                # Update password
                current_user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('main.profile'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error changing password: {str(e)}', 'error')
                return render_template('main/profile-change-password.html')
        
        return render_template('main/profile-change-password.html')

