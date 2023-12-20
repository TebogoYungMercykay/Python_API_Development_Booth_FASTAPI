"""add phone number

Revision ID: c47ecbf163d4
Revises: 036aa392dfb0
Create Date: 2021-08-29 23:42:58.021392

"""
from alembic import op
import sqlalchemy as sa

revision = 'c47ecbf163d4'
down_revision = '036aa392dfb0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'phone_number')
