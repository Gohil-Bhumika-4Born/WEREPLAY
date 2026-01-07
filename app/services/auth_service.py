"""
Authentication service for handling user authentication logic.
"""
from datetime import datetime, timedelta
from flask import current_app
from app.models.user import User, generate_app_name_id
from app.extensions import db
from app.services.email_service import EmailService


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
            tuple: (User object, error_code) where error_code is None if successful
                   Error codes: 'USER_NOT_FOUND', 'INVALID_PASSWORD', 'NOT_VERIFIED'
        """
        # Try to find user by email or username
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()
        
        if not user:
            return None, 'USER_NOT_FOUND'
        
        # Check if password is correct
        if not user.check_password(password):
            return None, 'INVALID_PASSWORD'
        
        # Check if user is verified
        if not user.is_verified:
            return None, 'NOT_VERIFIED'
        
        return user, None
    
    @staticmethod
    def register_user(username, email, phone, password):
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email address
            phone: User's phone number
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
        
        # Generate unique app_name_id
        max_retries = 10
        app_name_id = None
        for _ in range(max_retries):
            candidate_id = generate_app_name_id()
            if not User.query.filter_by(app_name_id=candidate_id).first():
                app_name_id = candidate_id
                break
        
        if not app_name_id:
            return None, "Failed to generate unique app ID. Please try again."

        # Create new user (unverified by default)
        user = User(username=username, email=email, phone=phone, is_verified=False, app_name_id=app_name_id)
        user.set_password(password)
        
        # Generate OTP and set expiration
        otp = EmailService.generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()
        user.otp_expires_at = datetime.utcnow() + timedelta(
            minutes=current_app.config.get('OTP_EXPIRY_MINUTES', 10)
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Send OTP email
            email_sent = EmailService.send_otp_email(email, otp, username)
            
            if not email_sent:
                # Log warning but don't fail registration
                print(f"Warning: Failed to send OTP email to {email}. OTP: {otp}")
            
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating user: {str(e)}"
    
    @staticmethod
    def verify_otp(user_id, otp):
        """
        Verify OTP code for user and mark as verified.
        
        Args:
            user_id: User ID
            otp: OTP code to verify
            
        Returns:
            True if OTP is valid, False otherwise
        """
        # Validate OTP format
        if not (otp and len(otp) == 6 and otp.isdigit()):
            return False
        
        # Get user and verify OTP
        user = User.query.get(user_id)
        if not user:
            return False
        
        # Use User model's is_otp_valid method
        if not user.is_otp_valid(otp):
            return False
        
        # Mark user as verified and clear OTP
        user.is_verified = True
        user.otp_code = None
        user.otp_created_at = None
        user.otp_expires_at = None
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def verify_password_reset_otp(user_id, otp):
        """
        Verify OTP code for password reset (does NOT change is_verified status).
        
        Args:
            user_id: User ID
            otp: OTP code to verify
            
        Returns:
            True if OTP is valid, False otherwise
        """
        # Validate OTP format
        if not (otp and len(otp) == 6 and otp.isdigit()):
            return False
        
        # Get user and verify OTP
        user = User.query.get(user_id)
        if not user:
            return False
        
        # Use User model's is_otp_valid method
        if not user.is_otp_valid(otp):
            return False
        
        # Clear OTP (but DON'T change is_verified status)
        user.otp_code = None
        user.otp_created_at = None
        user.otp_expires_at = None
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def resend_otp(user_id):
        """
        Resend OTP to user's email.
        
        Args:
            user_id: User ID
            
        Returns:
            True if OTP resent successfully, False otherwise
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        # Generate new OTP and update expiration
        otp = EmailService.generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()
        user.otp_expires_at = datetime.utcnow() + timedelta(
            minutes=current_app.config.get('OTP_EXPIRY_MINUTES', 10)
        )
        
        try:
            db.session.commit()
            
            # Send OTP email
            email_sent = EmailService.send_otp_email(user.email, otp, user.username)
            
            if not email_sent:
                print(f"Warning: Failed to resend OTP email to {user.email}. OTP: {otp}")
                return False
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error resending OTP: {str(e)}")
            return False
    
    @staticmethod
    def generate_login_otp(identifier):
        """
        Generate and send OTP for login.
        
        Args:
            identifier: Email or username
            
        Returns:
            User object if OTP sent successfully, None otherwise
        """
        # Find user by email or username
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()
        
        if not user:
            return None
        
        # Check if user is verified
        if not user.is_verified:
            return None
        
        # Generate OTP and set expiration
        otp = EmailService.generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()
        user.otp_expires_at = datetime.utcnow() + timedelta(
            minutes=current_app.config.get('OTP_EXPIRY_MINUTES', 10)
        )
        
        try:
            db.session.commit()
            
            # Send login OTP email
            email_sent = EmailService.send_login_otp_email(user.email, otp, user.username)
            
            if not email_sent:
                print(f"Warning: Failed to send login OTP email to {user.email}. OTP: {otp}")
                return None
            
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error generating login OTP: {str(e)}")
            return None
    
    @staticmethod
    def generate_password_reset_otp(email):
        """
        Generate and send OTP for password reset.
        
        Args:
            email: User's email address
            
        Returns:
            User object if OTP sent successfully, None otherwise
        """
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return None
        
        # Generate OTP and set expiration
        otp = EmailService.generate_otp()
        user.otp_code = otp
        user.otp_created_at = datetime.utcnow()
        user.otp_expires_at = datetime.utcnow() + timedelta(
            minutes=current_app.config.get('OTP_EXPIRY_MINUTES', 10)
        )
        
        try:
            db.session.commit()
            
            # Send password reset OTP email
            email_sent = EmailService.send_password_reset_otp_email(user.email, otp, user.username)
            
            if not email_sent:
                print(f"Warning: Failed to send password reset OTP email to {user.email}. OTP: {otp}")
                return None
            
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error generating password reset OTP: {str(e)}")
            return None
    
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
        
        # Set new password (hashed)
        user.set_password(new_password)
        
        # Clear OTP fields for security
        user.otp_code = None
        user.otp_created_at = None
        user.otp_expires_at = None
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
