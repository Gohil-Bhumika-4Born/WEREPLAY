"""
Plans model.
"""
from datetime import datetime
from app.extensions import db


class Plans(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)

    # CHANGED HERE: exact DB column names
    plan_name = db.Column(db.String(100), nullable=False)
    price_per_month = db.Column(db.Numeric(10, 2), nullable=False)
    free_trial = db.Column(db.String(50), nullable=True)
    ideal_for = db.Column(db.Text, nullable=False)

    # CHANGED HERE: renamed Documents Upload → tokens (as per your requirement)
    tokens = db.Column(db.Integer, nullable=False)

    api_integration = db.Column(db.String(255), nullable=False)
    ai_replies_per_month = db.Column(db.String(100), nullable=False)
    key_features = db.Column(db.Text, nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Plan {self.plan_name}>"
