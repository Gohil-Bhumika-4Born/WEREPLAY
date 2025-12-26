"""
Complete profile route.
"""
from . import auth_bp
from app.controllers.auth import CompleteProfileController


@auth_bp.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    """Complete profile page."""
    return CompleteProfileController.complete_profile_page()
