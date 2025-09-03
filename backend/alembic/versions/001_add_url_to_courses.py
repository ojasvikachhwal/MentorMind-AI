"""Add url field to courses table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add url column to courses table
    op.add_column('courses', sa.Column('url', sa.String(500), nullable=True))


def downgrade() -> None:
    # Remove url column from courses table
    op.drop_column('courses', 'url')
