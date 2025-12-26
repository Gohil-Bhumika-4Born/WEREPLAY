"""
AI Training controller for handling AI training-related requests.
"""
from flask import render_template
from flask_login import login_required


class AITrainingController:
    """Controller for AI training pages."""
    
    @staticmethod
    @login_required
    def ai_training_page():
        """Render AI training page."""
        return render_template('main/ai-training.html')
    
    @staticmethod
    @login_required
    def training_history_page():
        """Render training history page."""
        return render_template('main/training-history.html')
