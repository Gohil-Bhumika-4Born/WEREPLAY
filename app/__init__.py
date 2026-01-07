"""
Application factory for creating Flask app instances.
"""
import os
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager, mail


def create_app(config_name=None):
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Deprecated parameter, kept for backward compatibility.
                    Configuration is now loaded directly from environment variables.
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    @app.after_request
    def add_header(response):
        """
        Add cache control headers to prevent caching of sensitive pages.
        Applies strict no-cache policy to all auth routes to prevent back button navigation.
        """
        from flask import request
        
        # Define sensitive routes that should never be cached
        auth_routes = ['/auth/login', '/auth/register', '/auth/verify-otp', 
                      '/auth/complete-profile', '/auth/reset-password']
        
        # Check if current request path is an auth route
        if any(request.path.startswith(route) for route in auth_routes):
            # Strict no-cache headers for authentication pages
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        else:
            # Standard caching for other pages
            response.headers["Cache-Control"] = "public, max-age=300"
        
        return response
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app
