"""
API routes for general API endpoints.
"""
from . import main_bp
from app.controllers.main.api_controller import ApiController


@main_bp.route('/api/countries', methods=['GET'])
def get_countries():
    """Get all active countries."""
    return ApiController.get_countries()


@main_bp.route('/api/states/<int:country_id>', methods=['GET'])
def get_states(country_id):
    """Get all active states for a specific country."""
    return ApiController.get_states(country_id)
