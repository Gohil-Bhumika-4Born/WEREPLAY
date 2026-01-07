"""
Add app_name_id column to users table.

Revision ID: add_app_name_id_002
Revises: a1f6e15e0832
Create Date: 2026-01-06
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'add_app_name_id_002'
down_revision = 'a1f6e15e0832'
branch_labels = None
depends_on = None


def upgrade():
    """Add app_name_id column to users table (standalone, no foreign key)."""
    
    print("=" * 60)
    print("Adding app_name_id to users table...")
    print("=" * 60)
    
    # Add app_name_id column (nullable, standalone - no FK)
    op.add_column('users', sa.Column('app_name_id', sa.String(6), nullable=True))
    print("✓ Added app_name_id column")
    
    # Create index for better query performance
    try:
        op.create_index('idx_users_app_name_id', 'users', ['app_name_id'])
        print("✓ Created index on app_name_id")
    except Exception as e:
        print(f"⚠ Could not create index: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Migration completed!")
    print("=" * 60)
    print("app_name_id added as standalone column (no foreign key)")
    print("=" * 60)


def downgrade():
    """Remove app_name_id column from users table."""
    
    print("Reverting migration...")
    
    # Drop index
    try:
        op.drop_index('idx_users_app_name_id', table_name='users')
        print("✓ Dropped index")
    except:
        pass
    
    # Drop column
    op.drop_column('users', 'app_name_id')
    print("✓ Dropped app_name_id column")
    
    print("✅ Rollback completed!")
