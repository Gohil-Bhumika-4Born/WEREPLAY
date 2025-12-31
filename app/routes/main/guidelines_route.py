"""
Guidelines routes.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import GuidelinesController


@main_bp.route('/guidelines')
@profile_required
def guidelines():
    """Guidelines page."""
    return GuidelinesController.guidelines_new_page()


@main_bp.route('/guidelines-copy')
@profile_required
def guidelines_copy():
    """Guidelines copy page."""
    return GuidelinesController.guidelines_copy_page()
