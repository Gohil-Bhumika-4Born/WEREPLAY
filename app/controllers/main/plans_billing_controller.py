"""
Plans & Billing controller for handling plans and billing-related requests.
"""
from flask import render_template
from flask_login import login_required


class PlansBillingController:
    """Controller for plans and billing page."""
    
    @staticmethod
    @login_required
    def plans_billing_page():
        """Render plans and billing page."""
        return render_template('main/plans-billing.html')
