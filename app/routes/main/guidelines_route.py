"""
Guidelines routes.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import GuidelinesController


@main_bp.route('/guidelines')
@login_required
def guidelines():
    """Guidelines page."""
    return GuidelinesController.guidelines_new_page()


@main_bp.route('/guidelines-copy')
@login_required
def guidelines_copy():
    """Guidelines copy page."""
    return GuidelinesController.guidelines_copy_page()
