"""
Dashboard route.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import DashboardController


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page."""
    return DashboardController.dashboard_page()
