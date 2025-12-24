"""
Authentication service for handling user authentication logic.
"""
from app.models.user import User
from app.extensions import db


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def authenticate_user(identifier, password):
        """
        Authenticate a user with email/username and password.
        
        Args:
            identifier: Email or username
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # For now, use hardcoded authentication
        # TODO: Replace with database lookup when ready
        if identifier == 'admin@wereplay.com' and password == 'admin123':
            # Return a mock user object for now
            return {'email': identifier, 'username': 'admin'}
        return None
    
    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email address
            password: Plain text password
            
        Returns:
            User object if registration successful, error message otherwise
        """
        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            return None, "User with this email or username already exists"
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating user: {str(e)}"
    
    @staticmethod
    def verify_otp(user_id, otp):
        """
        Verify OTP code for user.
        
        Args:
            user_id: User ID
            otp: OTP code to verify
            
        Returns:
            True if OTP is valid, False otherwise
        """
        # TODO: Implement OTP verification logic
        # For now, accept any 6-digit code
        return len(otp) == 6 and otp.isdigit()
    
    @staticmethod
    def reset_password(user_id, new_password):
        """
        Reset user password.
        
        Args:
            user_id: User ID
            new_password: New plain text password
            
        Returns:
            True if password reset successful, False otherwise
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        user.set_password(new_password)
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
