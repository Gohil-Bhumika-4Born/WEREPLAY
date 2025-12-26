"""
Logout controller for handling logout-related requests.
"""
from flask import redirect, url_for, flash
from flask_login import logout_user


class LogoutController:
    """Controller for logout action."""
    
    @staticmethod
    def logout_action():
        """Handle logout action."""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
