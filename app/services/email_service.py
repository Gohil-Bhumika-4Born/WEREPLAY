"""
Email service for sending OTP and other emails.
"""
import random
from datetime import datetime, timedelta
from flask import current_app
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
            
            subject = "WeReply Admin Panel - Email Verification OTP"
            
            # Create HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        border-radius: 12px;
                        padding: 40px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #18CB96;
                        margin-bottom: 10px;
                    }}
                    .otp-box {{
                        background: linear-gradient(135deg, #18CB96 0%, #15b886 100%);
                        color: white;
                        font-size: 32px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        text-align: center;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 30px 0;
                    }}
                    .message {{
                        color: #666;
                        font-size: 16px;
                        margin: 20px 0;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 12px;
                        margin: 20px 0;
                        border-radius: 4px;
                        font-size: 14px;
                        color: #856404;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        color: #999;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">WeReply Admin Panel</div>
                        <h2 style="color: #333; margin: 0;">Email Verification</h2>
                    </div>
                    
                    <p class="message">
                        Hello{' ' + username if username else ''},
                    </p>
                    
                    <p class="message">
                        Thank you for registering with WeReply Admin Panel. To complete your registration, 
                        please use the following One-Time Password (OTP):
                    </p>
                    
                    <div class="otp-box">
                        {otp}
                    </div>
                    
                    <p class="message">
                        This OTP is valid for <strong>10 minutes</strong>. Please do not share this code with anyone.
                    </p>
                    
                    <div class="warning">
                        ⚠️ If you did not request this verification code, please ignore this email or contact our support team.
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated email. Please do not reply to this message.</p>
                        <p>&copy; 2025 WeReply. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version for email clients that don't support HTML
            text_body = f"""
            WeReply Admin Panel - Email Verification
            
            Hello{' ' + username if username else ''},
            
            Thank you for registering with WeReply Admin Panel. To complete your registration, 
            please use the following One-Time Password (OTP):
            
            {otp}
            
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
            subject = "WeReply Admin Panel - Login Verification OTP"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: #ffffff;
                        border-radius: 12px;
                        padding: 40px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #18CB96;
                        margin-bottom: 10px;
                    }}
                    .otp-box {{
                        background: linear-gradient(135deg, #18CB96 0%, #15b886 100%);
                        color: white;
                        font-size: 32px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        text-align: center;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 30px 0;
                    }}
                    .message {{
                        color: #666;
                        font-size: 16px;
                        margin: 20px 0;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 12px;
                        margin: 20px 0;
                        border-radius: 4px;
                        font-size: 14px;
                        color: #856404;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        color: #999;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">WeReply Admin Panel</div>
                        <h2 style="color: #333; margin: 0;">Login Verification</h2>
                    </div>
                    
                    <p class="message">
                        Hello{' ' + username if username else ''},
                    </p>
                    
                    <p class="message">
                        A login attempt was made to your WeReply Admin Panel account. 
                        Please use the following One-Time Password (OTP) to complete your login:
                    </p>
                    
                    <div class="otp-box">
                        {otp}
                    </div>
                    
                    <p class="message">
                        This OTP is valid for <strong>10 minutes</strong>. Please do not share this code with anyone.
                    </p>
                    
                    <div class="warning">
                        ⚠️ If you did not attempt to log in, please secure your account immediately and contact our support team.
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated email. Please do not reply to this message.</p>
                        <p>&copy; 2025 WeReply. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            WeReply Admin Panel - Login Verification
            
            Hello{' ' + username if username else ''},
            
            A login attempt was made to your WeReply Admin Panel account. 
            Please use the following One-Time Password (OTP) to complete your login:
            
            {otp}
            
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
