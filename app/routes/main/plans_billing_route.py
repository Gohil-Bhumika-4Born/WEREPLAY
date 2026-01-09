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


@main_bp.route('/plan-history')
@profile_required
def plan_history():
    """Plan history page."""
    return PlansBillingController.plan_history_page()
