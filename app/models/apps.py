"""
App model for wereply-backend.
This mirrors the apps table defined in Backend but provides local ORM access.
"""
from datetime import datetime
from app.extensions import db


class App(db.Model):
    """App model for storing application/tenant information."""
    
    __tablename__ = 'apps'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    app_name_id = db.Column(db.String(6), unique=True, nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert app to dictionary."""
        return {
            'id': self.id,
            'app_name': self.app_name,
            'app_name_id': self.app_name_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<App id={self.id} app_name={self.app_name} app_name_id={self.app_name_id}>'
