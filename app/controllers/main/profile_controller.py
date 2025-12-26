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
        """Render change password page."""
        return render_template('main/profile-change-password.html')
    
    @staticmethod
    def complete_profile_page():
        """Handle complete profile page GET and POST requests."""
        # Ensure user is logged in
        if not current_user.is_authenticated:
            flash('Please log in to complete your profile.', 'error')
            return redirect(url_for('auth.login'))
        
        # If profile already completed, redirect to dashboard
        if current_user.profile_completed:
            return redirect(url_for('main.dashboard'))
        
        if request.method == 'POST':
            # Update user profile with form data
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
            current_user.profile_completed = True
            
            try:
                db.session.commit()
                flash('Profile completed successfully!', 'success')
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving profile: {str(e)}', 'error')
        
        return render_template('main/complete-profile.html')
