"""
Documents controller for handling documents-related requests.
"""
from flask import render_template
from flask_login import login_required


class DocumentsController:
    """Controller for documents pages."""
    
    @staticmethod
    @login_required
    def documents_page():
        """Render documents page."""
        return render_template('main/documents.html')
    
    @staticmethod
    @login_required
    def documents_upload_page():
        """Render documents upload page."""
        return render_template('main/documents-upload.html')
