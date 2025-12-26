"""
Download Software route.
"""
from flask_login import login_required
from . import main_bp
from app.controllers.main import DownloadSoftwareController


@main_bp.route('/download-software')
@login_required
def download_software():
    """Download software page."""
    return DownloadSoftwareController.download_software_page()
