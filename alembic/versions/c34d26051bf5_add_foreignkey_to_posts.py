"""add foreignkey to posts

Revision ID: c34d26051bf5
Revises: ecaf5b4c6861
Create Date: 2023-02-17 15:33:01.333893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c34d26051bf5'
down_revision = 'ecaf5b4c6861'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable = False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
