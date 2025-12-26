"""
Profile routes.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import ProfileController


@main_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return ProfileController.profile_page()


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    """Profile edit page."""
    return ProfileController.profile_edit_page()


@main_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def profile_change_password():
    """Change password page."""
    return ProfileController.profile_change_password_page()


@main_bp.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    """Complete profile page."""
    return ProfileController.complete_profile_page()
