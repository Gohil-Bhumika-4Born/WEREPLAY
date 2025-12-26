"""
Chat Report model for storing conversation analytics.
"""
from datetime import datetime
from app.extensions import db


class ChatReport(db.Model):
    """Model for chat reports/conversation analytics."""
    
    __tablename__ = 'app_chat_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    message_count = db.Column(db.Integer, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False, index=True)
    category = db.Column(db.String(100), index=True)
    last_check_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatReport {self.id}: {self.title}>'
    
    def to_dict(self):
        """Convert chat report to dictionary."""
        return {
            'id': self.id,
            'app_id': self.app_id,
            'title': self.title,
            'description': self.description,
            'message_count': self.message_count,
            'sentiment': self.sentiment.upper(),
            'category': self.category,
            'last_check_time': self.last_check_time.strftime('%Y-%m-%d %H:%M') if self.last_check_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }
