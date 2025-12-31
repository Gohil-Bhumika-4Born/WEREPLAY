"""
Plans & Billing route.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import PlansBillingController


@main_bp.route('/plans-billing')
@profile_required
def plans_billing():
    """Plans and billing page."""
    return PlansBillingController.plans_billing_page()
