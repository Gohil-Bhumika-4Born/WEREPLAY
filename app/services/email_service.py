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
            # Debug logging - print email configuration
            print("\n" + "="*60)
            print("DEBUG: Email Configuration")
            print("="*60)
            print(f"MAIL_SERVER: {current_app.config.get('MAIL_SERVER')}")
            print(f"MAIL_PORT: {current_app.config.get('MAIL_PORT')}")
            print(f"MAIL_USE_TLS: {current_app.config.get('MAIL_USE_TLS')}")
            print(f"MAIL_USE_SSL: {current_app.config.get('MAIL_USE_SSL')}")
            print(f"MAIL_USERNAME: {current_app.config.get('MAIL_USERNAME')}")
            password = current_app.config.get('MAIL_PASSWORD')
            if password:
                print(f"MAIL_PASSWORD: {'*' * (len(password) - 4)}{password[-4:]} (length: {len(password)})")
            else:
                print("MAIL_PASSWORD: None or empty!")
            print(f"MAIL_DEFAULT_SENDER: {current_app.config.get('MAIL_DEFAULT_SENDER')}")
            print("="*60 + "\n")
            
            subject = "Your WeReply Verification Code"
            
            # Use the new email template
            html_body = render_template('email/otp-email.html', username=username, otp=otp)
            
            # Plain text version for email clients that don't support HTML
            text_body = f"""
            WeReply - Email Verification
            
            Hello{' ' + username if username else ''},
            
            We received a request to verify your email address. Please use the One-Time Password (OTP) below to complete your verification.
            
            Your Verification Code: {otp}
            
            This OTP is valid for 10 minutes. Please do not share this code with anyone.
            
            If you did not request this verification code, please ignore this email or contact our support team.
            
            This is an automated email. Please do not reply to this message.
            
            © 2025 WeReply. All rights reserved.
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            
            # Log success (for debugging)
            current_app.logger.info(f"OTP email sent successfully to {email}")
            
            return True
            
        except Exception as e:
            # Log error
            current_app.logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            print(f"Email Error: {str(e)}")
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
            
            # Use the new login email template
            html_body = render_template('email/login-otp-email.html', username=username, otp=otp)
            
            text_body = f"""
            WeReply - Login Verification
            
            Hello{' ' + username if username else ''},
            
            A login attempt was made to your WeReply account. 
            Please use the following One-Time Password (OTP) to complete your login:
            
            Your Login Code: {otp}
            
            This OTP is valid for 10 minutes. Please do not share this code with anyone.
            
            If you did not attempt to log in, please secure your account immediately and contact our support team.
            
            This is an automated email. Please do not reply to this message.
            
            © 2025 WeReply. All rights reserved.
            """
            
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
            print(f"Email Error: {str(e)}")
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
            
            # Use password reset email template (we'll create this)
            html_body = render_template('email/password-reset-otp-email.html', username=username, otp=otp)
            
            text_body = f"""
            WeReply - Password Reset
            
            Hello{' ' + username if username else ''},
            
            We received a request to reset your password. Please use the following One-Time Password (OTP) to continue:
            
            Your Password Reset Code: {otp}
            
            This OTP is valid for 10 minutes. Please do not share this code with anyone.
            
            If you did not request a password reset, please ignore this email or contact our support team.
            
            This is an automated email. Please do not reply to this message.
            
            © 2025 WeReply. All rights reserved.
            """
            
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
            print(f"Email Error: {str(e)}")
            return False
