"""change user_id to integer

Revision ID: 006
Revises: 005_create_users
Create Date: 2025-10-11 04:17:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005_create_users'
branch_labels = None
depends_on = None


def upgrade():
    # Сначала удаляем записи с нечисловым user_id (тестовые данные)
    op.execute("DELETE FROM tasks WHERE user_id !~ '^[0-9]+$'")
    
    # Теперь изменяем тип колонки user_id с String на Integer
    # Используем USING для преобразования существующих данных
    op.execute('ALTER TABLE tasks ALTER COLUMN user_id TYPE INTEGER USING user_id::integer')


def downgrade():
    # Возвращаем обратно к String
    op.execute('ALTER TABLE tasks ALTER COLUMN user_id TYPE VARCHAR USING user_id::varchar')
