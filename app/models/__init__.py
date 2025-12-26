"""
Models package initialization.
Exports all models for easy importing.
"""
from app.models.user import User
from app.models.chat_report import ChatReport

__all__ = ['User', 'ChatReport']
