"""
Plans & Billing route.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import PlansBillingController


@main_bp.route('/plans-billing')
@login_required
def plans_billing():
    """Plans and billing page."""
    return PlansBillingController.plans_billing_page()
