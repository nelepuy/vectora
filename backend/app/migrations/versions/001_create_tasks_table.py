from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String, nullable=False, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('deadline', sa.DateTime),
        sa.Column('status', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('tasks')
