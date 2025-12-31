"""
Chat Reports routes.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import ChatReportsController


@main_bp.route('/chat-reports')
@profile_required
def chat_reports():
    """Chat reports page."""
    return ChatReportsController.chat_reports_page()


@main_bp.route('/chat-reports/details')
@profile_required
def chat_reports_details():
    """Chat reports details page."""
    return ChatReportsController.chat_reports_details_page()
