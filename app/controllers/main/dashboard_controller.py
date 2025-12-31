"""
Dashboard controller for handling dashboard-related requests.
"""
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required


class DashboardController:
    """Controller for dashboard page."""
    
    @staticmethod
    @login_required
    def dashboard_page():
        """Render dashboard page."""
        # Check if user's email is verified
        if not current_user.is_verified:
            flash('Please verify your email to access the dashboard.', 'warning')
            return redirect(url_for('auth.verify_otp'))
        
        # Check if user has completed their profile
        if not current_user.profile_completed:
            flash('Please complete your profile to access the dashboard.', 'info')
            return redirect(url_for('auth.complete_profile'))
        
        return render_template('main/dashboard.html')
