"""
Email service for sending OTP and other emails.
"""
import random
from datetime import datetime, timedelta
from flask import current_app, render_template
from flask_mail import Mail, Message
from app.extensions import mail


class EmailService:
    """Service class for email operations."""
    
    @staticmethod
    def generate_otp():
        """
        Generate a random 6-digit OTP.
        
        Returns:
            String containing 6-digit OTP
        """
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_otp_email(email, otp, username=None):
        """
        Send OTP verification email to user.
        
        Args:
            email: Recipient email address
            otp: 6-digit OTP code
            username: Optional username for personalization
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = "Your WeReply Verification Code"
            
            # Use the HTML email template
            html_body = render_template('email/otp-email.html', username=username, otp=otp)
            
            # Simple plain text fallback for email clients that don't support HTML
            text_body = f"Your WeReply verification code is: {otp}. This code is valid for 10 minutes."
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            
            current_app.logger.info(f"OTP email sent successfully to {email}")
            
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            return False
    
    @staticmethod
    def send_login_otp_email(email, otp, username=None):
        """
        Send OTP for login verification.
        
        Args:
            email: Recipient email address
            otp: 6-digit OTP code
            username: Optional username for personalization
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = "Your WeReply Login Code"
            
            # Use the HTML email template
            html_body = render_template('email/login-otp-email.html', username=username, otp=otp)
            
            # Simple plain text fallback for email clients that don't support HTML
            text_body = f"Your WeReply login code is: {otp}. This code is valid for 10 minutes."
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            
            current_app.logger.info(f"Login OTP email sent successfully to {email}")
            
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send login OTP email to {email}: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_otp_email(email, otp, username=None):
        """
        Send OTP for password reset.
        
        Args:
            email: Recipient email address
            otp: 6-digit OTP code
            username: Optional username for personalization
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = "Your WeReply Password Reset Code"
            
            # Use the HTML email template
            html_body = render_template('email/password-reset-otp-email.html', username=username, otp=otp)
            
            # Simple plain text fallback for email clients that don't support HTML
            text_body = f"Your WeReply password reset code is: {otp}. This code is valid for 10 minutes."
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            
            current_app.logger.info(f"Password reset OTP email sent successfully to {email}")
            
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset OTP email to {email}: {str(e)}")
            return False
