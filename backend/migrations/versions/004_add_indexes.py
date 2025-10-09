"""add_database_indexes

Revision ID: 004_add_indexes
Revises: 003_add_categories_tags
Create Date: 2025-10-09

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_add_indexes'
down_revision = '003_add_categories_tags'
branch_labels = None
depends_on = None


def upgrade():
    # Создаем индексы для оптимизации запросов
    op.create_index('ix_tasks_title', 'tasks', ['title'])
    op.create_index('ix_tasks_date_time', 'tasks', ['date_time'])
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_tasks_category', 'tasks', ['category'])
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])


def downgrade():
    # Удаляем индексы при откате
    op.drop_index('ix_tasks_created_at', table_name='tasks')
    op.drop_index('ix_tasks_category', table_name='tasks')
    op.drop_index('ix_tasks_status', table_name='tasks')
    op.drop_index('ix_tasks_priority', table_name='tasks')
    op.drop_index('ix_tasks_date_time', table_name='tasks')
    op.drop_index('ix_tasks_title', table_name='tasks')
