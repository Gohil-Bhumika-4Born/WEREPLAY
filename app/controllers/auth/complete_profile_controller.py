"""
Complete profile controller for handling profile completion after registration.
"""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.extensions import db


class CompleteProfileController:
    """Controller for complete profile page and actions."""
    
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
            # Update basic information (allow user to modify name and phone)
            current_user.username = request.form.get('fullName')
            current_user.phone = request.form.get('phone')
            
            # Update business information
            current_user.business_name = request.form.get('businessName')
            current_user.business_category = request.form.get('businessCategory')
            current_user.website_url = request.form.get('websiteUrl')
            
            # Update address information
            current_user.country = request.form.get('country')
            current_user.state = request.form.get('state')
            current_user.city = request.form.get('city')
            current_user.pincode = request.form.get('pincode')
            
            # Update profile settings
            current_user.timezone = request.form.get('timezone')
            current_user.preferred_language = request.form.get('preferredLanguage')
            current_user.notification_preference = request.form.get('notificationPreference')
            
            # Mark profile as completed
            current_user.profile_completed = True
            
            try:
                db.session.commit()
                flash('Profile completed successfully!', 'success')
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving profile: {str(e)}', 'error')
        
        return render_template('auth/complete-profile.html', user=current_user)
