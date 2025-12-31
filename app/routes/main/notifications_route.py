"""
Notifications route.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import NotificationsController


@main_bp.route('/notifications')
@profile_required
def notifications():
    """Notifications page."""
    return NotificationsController.notifications_page()
