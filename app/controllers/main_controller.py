"""
Main application controller for handling main application pages.
"""
from flask import render_template


class MainController:
    """Controller for main application pages."""
    
    @staticmethod
    def dashboard_page():
        """Render dashboard page."""
        return render_template('main/dashboard.html')
    
    @staticmethod
    def profile_page():
        """Render user profile page."""
        return render_template('main/profile.html')
    
    @staticmethod
    def profile_edit_page():
        """Render profile edit page."""
        return render_template('main/profile-edit.html')
    
    @staticmethod
    def profile_change_password_page():
        """Render change password page."""
        return render_template('main/profile-change-password.html')
    
    @staticmethod
    def complete_profile_page():
        """Render complete profile page."""
        return render_template('main/complete-profile.html')
    
    @staticmethod
    def documents_page():
        """Render documents page."""
        return render_template('main/documents.html')
    
    @staticmethod
    def documents_upload_page():
        """Render documents upload page."""
        return render_template('main/documents-upload.html')
    
    @staticmethod
    def ai_training_page():
        """Render AI training page."""
        return render_template('main/ai-training.html')
    
    @staticmethod
    def training_history_page():
        """Render training history page."""
        return render_template('main/training-history.html')
    
    @staticmethod
    def chat_reports_page():
        """Render chat reports page."""
        return render_template('main/chat-reports.html')
    
    @staticmethod
    def chat_reports_details_page():
        """Render chat reports details page."""
        return render_template('main/chat-reports-details.html')
    
    @staticmethod
    def guidelines_new_page():
        """Render guidelines page."""
        return render_template('main/guidelines-new.html')
    
    @staticmethod
    def guidelines_copy_page():
        """Render guidelines copy page."""
        return render_template('main/guidelines_copy.html')
    
    @staticmethod
    def notifications_page():
        """Render notifications page."""
        return render_template('main/notifications.html')
    
    @staticmethod
    def plans_billing_page():
        """Render plans and billing page."""
        return render_template('main/plans-billing.html')
    
    @staticmethod
    def download_software_page():
        """Render download software page."""
        return render_template('main/download-software.html')
    
    @staticmethod
    def support_page():
        """Render support page."""
        return render_template('main/support.html')
