"""
Support controller for handling support-related requests.
"""
from flask import render_template
from flask_login import login_required


class SupportController:
    """Controller for support page."""
    
    @staticmethod
    @login_required
    def support_page():
        """Render support page."""
        return render_template('main/support.html')
