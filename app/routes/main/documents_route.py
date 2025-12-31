"""
Documents routes.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import DocumentsController


@main_bp.route('/documents')
@profile_required
def documents():
    """Documents page."""
    return DocumentsController.documents_page()


@main_bp.route('/documents/upload', methods=['GET', 'POST'])
@profile_required
def documents_upload():
    """Documents upload page."""
    return DocumentsController.documents_upload_page()
