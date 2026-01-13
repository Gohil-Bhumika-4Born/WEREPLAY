"""
Models package initialization.
Exports all models for easy importing.
"""
from app.models.user import User
from app.models.chat_report import ChatReport
from app.models.apps import App
from app.models.plans import Plans   # CHANGED HERE
from app.models.documents import Document


__all__ = ['User', 'ChatReport', 'App','Plans', 'Document']
