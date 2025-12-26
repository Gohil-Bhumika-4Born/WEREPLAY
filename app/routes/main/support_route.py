"""
Support route.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import SupportController


@main_bp.route('/support')
@login_required
def support():
    """Support page."""
    return SupportController.support_page()
