"""
User model for authentication and user management.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db
import random
import string

def generate_app_name_id():
    """Generate a random 6-character ID for app_name_id."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))



class User(UserMixin, db.Model):
    """User model for storing user account information."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # App Association (standalone field, no foreign key)
    app_name_id = db.Column(db.String(6), nullable=True, index=True)
    
    # Business Information
    business_name = db.Column(db.String(255), nullable=True)
    business_category = db.Column(db.String(100), nullable=True)
    website_url = db.Column(db.String(500), nullable=True)
    
    # Address Information
    country = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(20), nullable=True)
    
    # Profile Settings
    timezone = db.Column(db.String(50), nullable=True, default='utc')
    preferred_language = db.Column(db.String(10), nullable=True, default='en')
    notification_preference = db.Column(db.String(50), nullable=True, default='email')
    
    # Profile Completion Tracking
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # OTP Fields for email verification and login
    otp_code = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    otp_expires_at = db.Column(db.DateTime, nullable=True)

    #plan_id added
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    plan = db.relationship('Plans', backref='users')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_otp_valid(self, otp):
        """
        Check if the provided OTP is valid and not expired.
        
        Args:
            otp: OTP code to verify
            
        Returns:
            True if OTP is valid and not expired, False otherwise
        """
        if not self.otp_code or not self.otp_expires_at:
            return False
        
        # Check if OTP matches
        if self.otp_code != otp:
            return False
        
        # Check if OTP has expired
        if datetime.utcnow() > self.otp_expires_at:
            return False
        
        return True
    
    def __repr__(self):
        return f'<User {self.username}>'
