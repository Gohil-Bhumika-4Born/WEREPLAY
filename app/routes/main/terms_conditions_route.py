"""
Terms & Conditions route.
"""
from . import main_bp
from app.controllers.main import TermsConditionsController


@main_bp.route('/terms-conditions')
def terms_conditions():
    """Terms and conditions page."""
    return TermsConditionsController.terms_conditions_page()
