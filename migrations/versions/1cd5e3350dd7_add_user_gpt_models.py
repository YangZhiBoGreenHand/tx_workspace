"""add_user_gpt_models

Revision ID: 1cd5e3350dd7
Revises: 
Create Date: 2023-12-17 22:40:10.692373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cd5e3350dd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.create_index('idx_topic_user_history', ['topic_id', 'user_id'], unique=False)

    op.create_table('topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.create_index('idx_user_id_topics', ['user_id'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('idx_unique_phone_number', ['phone_number'], unique=True)

    op.create_table('workspaces',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('tenant_id', sa.String(length=255), nullable=True),
    sa.Column('ui_settings', sa.JSON(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('create_by', sa.String(length=255), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workspaces')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('idx_unique_phone_number')

    op.drop_table('users')
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_index('idx_user_id_topics')

    op.drop_table('topics')
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_index('idx_topic_user_history')

    op.drop_table('history')
    # ### end Alembic commands ###