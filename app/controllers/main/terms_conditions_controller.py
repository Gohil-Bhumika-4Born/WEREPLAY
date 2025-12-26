"""
Terms & Conditions controller for handling terms and conditions-related requests.
"""
from flask import render_template


class TermsConditionsController:
    """Controller for terms and conditions page."""
    
    @staticmethod
    def terms_conditions_page():
        """Render terms and conditions page."""
        return render_template('main/terms-conditions.html')
