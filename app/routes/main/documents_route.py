"""
Documents routes.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import DocumentsController
from flask import request


@main_bp.route('/documents')
@profile_required
def documents():
    """Documents page."""
    # CHANGED HERE: list documents page only
    return DocumentsController.documents_page()


@main_bp.route('/documents/upload', methods=['GET', 'POST'])
@profile_required
def documents_upload():
    """Documents upload page + handler."""
    # CHANGED HERE: separate GET and POST behavior
    if request.method == 'POST':
        return DocumentsController.upload_document()

    return DocumentsController.documents_upload_page()
