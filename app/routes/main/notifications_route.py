"""
Notifications route.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import NotificationsController


@main_bp.route('/notifications')
@login_required
def notifications():
    """Notifications page."""
    return NotificationsController.notifications_page()
