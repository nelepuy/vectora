"""add recurring tasks and subtasks

Revision ID: 007
Revises: 006
Create Date: 2025-10-11 04:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('parent_task_id', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('recurrence_type', sa.String(), nullable=True))
    op.add_column('tasks', sa.Column('recurrence_interval', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('next_occurrence', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('reminder_enabled', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('tasks', sa.Column('reminder_minutes_before', sa.Integer(), server_default='30', nullable=False))
    
    op.create_index(op.f('ix_tasks_parent_task_id'), 'tasks', ['parent_task_id'], unique=False)
    op.create_foreign_key('fk_tasks_parent', 'tasks', 'tasks', ['parent_task_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('fk_tasks_parent', 'tasks', type_='foreignkey')
    op.drop_index(op.f('ix_tasks_parent_task_id'), table_name='tasks')
    op.drop_column('tasks', 'reminder_minutes_before')
    op.drop_column('tasks', 'reminder_enabled')
    op.drop_column('tasks', 'next_occurrence')
    op.drop_column('tasks', 'recurrence_interval')
    op.drop_column('tasks', 'recurrence_type')
    op.drop_column('tasks', 'parent_task_id')
