"""
Custom authentication decorators for protecting routes.
"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, login_required


def profile_required(f):
    """
    Decorator that ensures user is authenticated, verified, and has completed profile.
    
    This decorator should be used on routes that require full user setup.
    It checks:
    1. User is authenticated (logged in)
    2. User has verified their email (is_verified = True)
    3. User has completed their profile (profile_completed = True)
    
    If any check fails, user is redirected to the appropriate page:
    - Not authenticated -> login page
    - Not verified -> OTP verification page
    - Profile incomplete -> complete profile page
    
    Usage:
        @app.route('/protected-page')
        @profile_required
        def protected_page():
            return render_template('protected.html')
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # At this point, user is authenticated (ensured by @login_required)
        
        # Check if user's email is verified
        if not current_user.is_verified:
            flash('Please verify your email to access this page.', 'warning')
            return redirect(url_for('auth.verify_otp'))
        
        # Check if user has completed their profile
        if not current_user.profile_completed:
            flash('Please complete your profile to access this page.', 'info')
            return redirect(url_for('auth.complete_profile'))
        
        # All checks passed, proceed with the original function
        return f(*args, **kwargs)
    
    return decorated_function
