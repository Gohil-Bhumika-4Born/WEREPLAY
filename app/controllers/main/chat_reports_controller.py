"""
Chat Reports controller for handling chat reports-related requests.
"""
from flask import render_template
from flask_login import login_required


class ChatReportsController:
    """Controller for chat reports pages."""
    
    @staticmethod
    @login_required
    def chat_reports_page():
        """Render chat reports page with data from database."""
        from app.models.chat_report import ChatReport
        
        # Fetch all chat reports from database
        chat_reports = ChatReport.query.order_by(ChatReport.updated_at.desc()).all()
        
        # Convert to list of dictionaries for JSON serialization
        reports_data = [report.to_dict() for report in chat_reports]
        
        return render_template('main/chat-reports.html', chat_reports=reports_data)
    
    @staticmethod
    @login_required
    def chat_reports_details_page():
        """Render chat reports details page."""
        return render_template('main/chat-reports-details.html')
