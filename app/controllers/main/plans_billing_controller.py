"""
Plans & Billing controller for handling plans and billing-related requests.
"""
from flask import render_template
from flask_login import login_required
from app.models.plans import Plans


class PlansBillingController:
    """Controller for plans and billing pages."""

    @staticmethod
    @login_required
    def plans_billing_page():
        """Render plans and billing page."""
        plans = (
            Plans.query
            .filter_by(is_active=1)
            .order_by(Plans.price_per_month)
            .all()
        )

        return render_template(
            'main/plans-billing.html',
            plans=plans
        )

    # ADDED: plan history page controller
    @staticmethod
    @login_required
    def plan_history_page():
        """Render plan history page."""
        return render_template('main/plan-history.html')
