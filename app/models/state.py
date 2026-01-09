"""
State model for geographic lookups.
"""
from app.extensions import db


class State(db.Model):
    """State model for storing state/province information."""
    
    __tablename__ = 'state'
    
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    def to_dict(self):
        """Convert state to dictionary."""
        return {
            'id': self.id,
            'country_id': self.country_id,
            'name': self.name,
            'code': self.code
        }
    
    def __repr__(self):
        return f'<State {self.name} ({self.code})>'
