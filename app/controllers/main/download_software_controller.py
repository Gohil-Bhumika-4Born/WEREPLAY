"""
Download Software controller for handling download software-related requests.
"""
from flask import render_template
from flask_login import login_required


class DownloadSoftwareController:
    """Controller for download software page."""
    
    @staticmethod
    @login_required
    def download_software_page():
        """Render download software page."""
        return render_template('main/download-software.html')
