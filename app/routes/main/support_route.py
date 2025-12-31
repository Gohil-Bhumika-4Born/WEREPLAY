"""
Support route.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import SupportController


@main_bp.route('/support')
@profile_required
def support():
    """Support page."""
    return SupportController.support_page()
