"""
API controller for general API endpoints.
"""
from flask import jsonify
from app.models.country import Country
from app.models.state import State


class ApiController:
    """Controller for API endpoints."""
    
    @staticmethod
    def get_countries():
        """
        Get all active countries.
        
        Returns:
            JSON response with list of countries
        """
        try:
            # Query all active countries, ordered by name
            countries = Country.query.filter_by(status=1).order_by(Country.name).all()
            
            return jsonify({
                'success': True,
                'countries': [country.to_dict() for country in countries]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def get_states(country_id):
        """
        Get all active states for a specific country.
        
        Args:
            country_id: ID of the country
            
        Returns:
            JSON response with list of states
        """
        try:
            # Query all active states for the country, ordered by name
            states = State.query.filter_by(
                country_id=country_id,
                status=1
            ).order_by(State.name).all()
            
            return jsonify({
                'success': True,
                'states': [state.to_dict() for state in states]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
