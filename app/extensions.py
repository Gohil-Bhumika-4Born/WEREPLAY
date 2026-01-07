"""
Flask extensions initialization.
Extensions are initialized here and then attached to the app in the factory.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for Flask-Login.
    This callback is used to reload the user object from the user ID stored in the session.
    """
    from app.models.user import User
    return User.query.get(int(user_id))
