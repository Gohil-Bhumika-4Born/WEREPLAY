"""
Country model for geographic lookups.
"""
from app.extensions import db


class Country(db.Model):
    """Country model for storing country information."""
    
    __tablename__ = 'country'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    iso_code_2 = db.Column(db.String(2), nullable=False)
    iso_code_3 = db.Column(db.String(3), nullable=False)
    address_format = db.Column(db.Text, nullable=False)
    postcode_required = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    def to_dict(self):
        """Convert country to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'iso_code_2': self.iso_code_2,
            'iso_code_3': self.iso_code_3
        }
    
    def __repr__(self):
        return f'<Country {self.name} ({self.iso_code_2})>'
