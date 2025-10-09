"""create users table and update tasks

Revision ID: 005_create_users
Revises: 004_add_indexes
Create Date: 2025-10-09

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_create_users'
down_revision = '004_add_indexes'
branch_labels = None
depends_on = None


def upgrade():
    # Создаем таблицу users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_admin', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создаем индексы для users
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_telegram_id', 'users', ['telegram_id'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_created_at', 'users', ['created_at'])
    
    # Создаем временную таблицу задач с новой структурой
    op.create_table(
        'tasks_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date_time', sa.DateTime(), nullable=True),
        sa.Column('priority', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Копируем индексы
    op.create_index('ix_tasks_new_id', 'tasks_new', ['id'])
    op.create_index('ix_tasks_new_user_id', 'tasks_new', ['user_id'])
    op.create_index('ix_tasks_new_title', 'tasks_new', ['title'])
    op.create_index('ix_tasks_new_date_time', 'tasks_new', ['date_time'])
    op.create_index('ix_tasks_new_priority', 'tasks_new', ['priority'])
    op.create_index('ix_tasks_new_status', 'tasks_new', ['status'])
    op.create_index('ix_tasks_new_category', 'tasks_new', ['category'])
    op.create_index('ix_tasks_new_created_at', 'tasks_new', ['created_at'])


def downgrade():
    # Удаляем новую таблицу tasks
    op.drop_index('ix_tasks_new_created_at', table_name='tasks_new')
    op.drop_index('ix_tasks_new_category', table_name='tasks_new')
    op.drop_index('ix_tasks_new_status', table_name='tasks_new')
    op.drop_index('ix_tasks_new_priority', table_name='tasks_new')
    op.drop_index('ix_tasks_new_date_time', table_name='tasks_new')
    op.drop_index('ix_tasks_new_title', table_name='tasks_new')
    op.drop_index('ix_tasks_new_user_id', table_name='tasks_new')
    op.drop_index('ix_tasks_new_id', table_name='tasks_new')
    op.drop_table('tasks_new')
    
    # Удаляем таблицу users
    op.drop_index('ix_users_created_at', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_telegram_id', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
