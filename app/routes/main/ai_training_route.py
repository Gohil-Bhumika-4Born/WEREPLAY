"""
AI Training routes.
"""
from app.utils import profile_required
from . import main_bp
from app.controllers.main import AITrainingController


@main_bp.route('/ai-training')
@profile_required
def ai_training():
    """AI training page."""
    return AITrainingController.ai_training_page()


@main_bp.route('/training-history')
@profile_required
def training_history():
    """Training history page."""
    return AITrainingController.training_history_page()
