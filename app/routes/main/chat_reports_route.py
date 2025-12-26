"""
Chat Reports routes.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import ChatReportsController


@main_bp.route('/chat-reports')
@login_required
def chat_reports():
    """Chat reports page."""
    return ChatReportsController.chat_reports_page()


@main_bp.route('/chat-reports/details')
@login_required
def chat_reports_details():
    """Chat reports details page."""
    return ChatReportsController.chat_reports_details_page()
