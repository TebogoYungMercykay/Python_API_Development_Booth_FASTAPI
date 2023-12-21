"""auto-vote

Revision ID: 036aa392dfb0
Revises: 036d0a4565b7
Create Date: 2023-12-21 22:50:42.028498

"""
from alembic import op
import sqlalchemy as sa

revision = '036aa392dfb0'
down_revision = '036d0a4565b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )

def downgrade():
    op.drop_table('votes')
