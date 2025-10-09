"""add updated_at column to tasks

Revision ID: 002
Revises: 001
Create Date: 2025-09-22 19:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('tasks', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('tasks', 'updated_at')
