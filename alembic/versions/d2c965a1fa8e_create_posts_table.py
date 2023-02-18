"""create posts table

Revision ID: d2c965a1fa8e
Revises: 
Create Date: 2023-02-17 14:51:38.059409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2c965a1fa8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable = False, primary_key = True), 
                             sa.Column('title', sa.String(), nullable = False))


def downgrade():
    op.drop_table("posts")

