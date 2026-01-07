"""
Dashboard route.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import DashboardController


@main_bp.route('/dashboard')
@profile_required
def dashboard():
    """Dashboard page."""
    return DashboardController.dashboard_page()
