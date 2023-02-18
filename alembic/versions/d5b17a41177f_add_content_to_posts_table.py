"""add content to posts table

Revision ID: d5b17a41177f
Revises: d2c965a1fa8e
Create Date: 2023-02-17 15:15:10.826650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b17a41177f'
down_revision = 'd2c965a1fa8e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
