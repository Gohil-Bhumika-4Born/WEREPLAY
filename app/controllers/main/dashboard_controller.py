"""
Dashboard controller for handling dashboard-related requests.
"""
from flask import render_template
from flask_login import login_required


class DashboardController:
    """Controller for dashboard page."""
    
    @staticmethod
    @login_required
    def dashboard_page():
        """Render dashboard page."""
        return render_template('main/dashboard.html')
