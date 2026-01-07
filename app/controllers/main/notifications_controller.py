"""
Notifications controller for handling notifications-related requests.
"""
from flask import render_template
from flask_login import login_required


class NotificationsController:
    """Controller for notifications page."""
    
    @staticmethod
    @login_required
    def notifications_page():
        """Render notifications page."""
        return render_template('main/notifications.html')
