"""
Main application routes blueprint.
Handles all main application URLs.
"""
from flask import Blueprint
from app.controllers.main_controller import MainController

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page."""
    return MainController.dashboard_page()


@main_bp.route('/profile')
def profile():
    """User profile page."""
    return MainController.profile_page()


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    """Profile edit page."""
    return MainController.profile_edit_page()


@main_bp.route('/profile/change-password', methods=['GET', 'POST'])
def profile_change_password():
    """Change password page."""
    return MainController.profile_change_password_page()


@main_bp.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    """Complete profile page."""
    return MainController.complete_profile_page()


@main_bp.route('/documents')
def documents():
    """Documents page."""
    return MainController.documents_page()


@main_bp.route('/documents/upload', methods=['GET', 'POST'])
def documents_upload():
    """Documents upload page."""
    return MainController.documents_upload_page()


@main_bp.route('/ai-training')
def ai_training():
    """AI training page."""
    return MainController.ai_training_page()


@main_bp.route('/training-history')
def training_history():
    """Training history page."""
    return MainController.training_history_page()


@main_bp.route('/chat-reports')
def chat_reports():
    """Chat reports page."""
    return MainController.chat_reports_page()


@main_bp.route('/chat-reports/details')
def chat_reports_details():
    """Chat reports details page."""
    return MainController.chat_reports_details_page()


@main_bp.route('/guidelines')
def guidelines():
    """Guidelines page."""
    return MainController.guidelines_new_page()


@main_bp.route('/guidelines-copy')
def guidelines_copy():
    """Guidelines copy page."""
    return MainController.guidelines_copy_page()


@main_bp.route('/notifications')
def notifications():
    """Notifications page."""
    return MainController.notifications_page()


@main_bp.route('/plans-billing')
def plans_billing():
    """Plans and billing page."""
    return MainController.plans_billing_page()


@main_bp.route('/download-software')
def download_software():
    """Download software page."""
    return MainController.download_software_page()


@main_bp.route('/support')
def support():
    """Support page."""
    return MainController.support_page()
