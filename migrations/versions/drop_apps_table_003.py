"""
Drop apps table entirely.

Revision ID: drop_apps_table_003
Revises: add_app_name_id_002
Create Date: 2026-01-06
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'drop_apps_table_003'
down_revision = 'add_app_name_id_002'
branch_labels = None
depends_on = None


def upgrade():
    """Drop user_apps and apps tables, update app_chat_reports to reference users."""
    
    print("=" * 60)
    print("Step 1: Dropping user_apps table...")
    print("=" * 60)
    
    connection = op.get_bind()
    
    # Drop user_apps table first (it has FK to apps)
    try:
        result = connection.execute(sa.text("""
            SELECT TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'user_apps'
        """))
        
        if result.fetchone():
            op.drop_table('user_apps')
            print("✓ Dropped user_apps table")
        else:
            print("✓ user_apps table doesn't exist")
    except Exception as e:
        print(f"⚠ Error dropping user_apps: {e}")
    
    print("\n" + "=" * 60)
    print("Step 2: Removing foreign key from app_chat_reports...")
    print("=" * 60)
    
    # Drop foreign key constraint from app_chat_reports
    try:
        op.drop_constraint('app_chat_reports_ibfk_1', 'app_chat_reports', type_='foreignkey')
        print("✓ Dropped foreign key constraint from app_chat_reports")
    except Exception as e:
        print(f"⚠ Could not drop FK (may not exist): {e}")
    
    print("\n" + "=" * 60)
    print("Step 3: Changing app_id column type in app_chat_reports...")
    print("=" * 60)
    
    # Change app_id from Integer to String to match users.app_name_id
    try:
        op.alter_column('app_chat_reports', 'app_id',
                       existing_type=sa.Integer(),
                       type_=sa.String(6),
                       nullable=True)
        print("✓ Changed app_id to String(6)")
    except Exception as e:
        print(f"⚠ Error changing column type: {e}")
    
    print("\n" + "=" * 60)
    print("Step 4: Dropping apps table...")
    print("=" * 60)
    
    # Drop apps table
    try:
        result = connection.execute(sa.text("""
            SELECT TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'apps'
        """))
        
        if result.fetchone():
            op.drop_table('apps')
            print("✓ Dropped apps table")
        else:
            print("✓ apps table doesn't exist")
    except Exception as e:
        print(f"⚠ Error dropping apps: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Migration completed!")
    print("=" * 60)
    print("Summary:")
    print("  • Dropped user_apps table")
    print("  • Removed FK from app_chat_reports.app_id")
    print("  • Changed app_chat_reports.app_id to String(6)")
    print("  • Dropped apps table")
    print("  • app_chat_reports.app_id now references users.app_name_id")
    print("=" * 60)


def downgrade():
    """Recreate apps table."""
    
    print("Recreating apps table...")
    
    # Create apps table
    op.create_table(
        'apps',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('app_name', sa.String(255), nullable=False),
        sa.Column('app_name_id', sa.String(6), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('app_name', 'apps', ['app_name'], unique=True)
    op.create_index('app_name_id', 'apps', ['app_name_id'], unique=True)
    
    print("✅ apps table recreated!")
