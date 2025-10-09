"""add categories and tags to tasks

Revision ID: 003_add_categories_tags
Revises: 002
Create Date: 2024-12-24 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = '003_add_categories_tags'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Добавляем поле category
    op.add_column('tasks', sa.Column('category', sa.String(), nullable=True))
    
    # Добавляем поле tags (JSON для списка тегов)
    op.add_column('tasks', sa.Column('tags', JSON, nullable=True, server_default='[]'))


def downgrade() -> None:
    # Удаляем добавленные колонки
    op.drop_column('tasks', 'tags')
    op.drop_column('tasks', 'category')
