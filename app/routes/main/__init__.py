"""
Main application routes package.
"""
from flask import Blueprint

# Create blueprint
main_bp = Blueprint('main', __name__)



# Import all route modules to register them with the blueprint
from . import (
    dashboard_route,
    profile_route,
    documents_route,
    ai_training_route,
    chat_reports_route,
    guidelines_route,
    notifications_route,
    plans_billing_route,
    download_software_route,
    support_route,
    terms_conditions_route
)

__all__ = ['main_bp']
