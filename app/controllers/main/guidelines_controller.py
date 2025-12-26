"""
Guidelines controller for handling guidelines-related requests.
"""
from flask import render_template
from flask_login import login_required


class GuidelinesController:
    """Controller for guidelines pages."""
    
    @staticmethod
    @login_required
    def guidelines_new_page():
        """Render guidelines page."""
        return render_template('main/guidelines-new.html')
    
    @staticmethod
    @login_required
    def guidelines_copy_page():
        """Render guidelines copy page."""
        return render_template('main/guidelines_copy.html')
