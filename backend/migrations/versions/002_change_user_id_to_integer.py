"""change user_id to integer

Revision ID: 002
Revises: 001
Create Date: 2025-10-11 04:17:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Изменяем тип колонки user_id с String на Integer
    # Используем USING для преобразования существующих данных
    op.execute('ALTER TABLE tasks ALTER COLUMN user_id TYPE INTEGER USING user_id::integer')


def downgrade():
    # Возвращаем обратно к String
    op.execute('ALTER TABLE tasks ALTER COLUMN user_id TYPE VARCHAR USING user_id::varchar')
