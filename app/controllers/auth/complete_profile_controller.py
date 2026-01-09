"""
Complete profile controller for handling profile completion after registration.
"""
from flask import render_template, request, redirect, url_for, flash, session
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
            
        errors = {}
        form_data = {}
        
        if request.method == 'POST':
            # Collect form data
            form_data = {
                'fullName': request.form.get('fullName'),
                'phone': request.form.get('phone'),
                'businessName': request.form.get('businessName'),
                'businessCategory': request.form.get('businessCategory'),
                'websiteUrl': request.form.get('websiteUrl'),
                'country': request.form.get('country'),
                'state': request.form.get('state'),
                'city': request.form.get('city'),
                'pincode': request.form.get('pincode'),
                'timezone': request.form.get('timezone'),
                'preferredLanguage': request.form.get('preferredLanguage'),
                'notificationPreference': request.form.get('notificationPreference')
            }
            
            # Validation - collect all missing/invalid fields
            missing_fields = []
            
            if not form_data['fullName'] or len(form_data['fullName'].strip()) < 3:
                missing_fields.append('Full name')
                
            if not form_data['phone']:
                missing_fields.append('Phone number')
            elif not form_data['phone'].isdigit() or len(form_data['phone']) < 10 or len(form_data['phone']) > 15:
                flash('Please enter a valid phone number (10-15 digits).', 'error')
                return render_template('auth/complete-profile.html', user=current_user, form_data=form_data)
                
            if not form_data['businessName'] or len(form_data['businessName'].strip()) < 2:
                missing_fields.append('Business name')
                
            if not form_data['businessCategory']:
                missing_fields.append('Business category')
                
            if not form_data['country']:
                missing_fields.append('Country')
                
            if not form_data['state']:
                missing_fields.append('State')
                
            if not form_data['city']:
                missing_fields.append('City')
                
            if not form_data['pincode']:
                missing_fields.append('Pincode')
                
            if not form_data['timezone']:
                missing_fields.append('Timezone')
                
            if not form_data['preferredLanguage']:
                missing_fields.append('Preferred language')
                
            if not form_data['notificationPreference']:
                missing_fields.append('Notification preference')

            # If there are missing fields, flash a single combined error message
            if missing_fields:
                if len(missing_fields) == 1:
                    error_message = f'Please fill in {missing_fields[0]}.'
                else:
                    error_message = f'Please fill in the following fields: {", ".join(missing_fields)}.'
                flash(error_message, 'error')
                return render_template('auth/complete-profile.html', user=current_user, form_data=form_data)
            
            # Update basic information
            current_user.username = form_data['fullName']
            current_user.phone = form_data['phone']
            
            # Update business information
            current_user.business_name = form_data['businessName']
            current_user.business_category = form_data['businessCategory']
            current_user.website_url = form_data['websiteUrl']
            
            # Update address information
            current_user.country = form_data['country']
            current_user.state = form_data['state']
            current_user.city = form_data['city']
            current_user.pincode = form_data['pincode']
            
            # Update profile settings
            current_user.timezone = form_data['timezone']
            current_user.preferred_language = form_data['preferredLanguage']
            current_user.notification_preference = form_data['notificationPreference']
            
            # Mark profile as completed
            current_user.profile_completed = True
            
            try:
                db.session.commit()
                
                # Clear all authentication flow session flags
                session.pop('registration_complete', None)
                session.pop('otp_verified', None)
                
                # Refresh session to ensure user stays logged in
                from flask_login import login_user
                login_user(current_user, remember=True)
                
                flash('Profile completed successfully!', 'success')
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving profile: {str(e)}', 'error')
                return render_template('auth/complete-profile.html', user=current_user, errors={'general': str(e)}, form_data=form_data)
        
        return render_template('auth/complete-profile.html', user=current_user, form_data={})
