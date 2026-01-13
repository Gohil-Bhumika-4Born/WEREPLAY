"""
Document model.
"""
from datetime import datetime
from app.extensions import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)

    # Document info
    document_title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)

    # File storage
    document_path = db.Column(db.String(500), nullable=False)

    # CHANGED HERE: REQUIRED metadata for preview & listing
    file_type = db.Column(db.String(20), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # stored in bytes
    extracted_text = db.Column(db.Text, nullable=True)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Meta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship('User', backref='documents')

    def __repr__(self):
        return f"<Document {self.document_title}>"
