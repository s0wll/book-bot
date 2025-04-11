"""add users

Revision ID: 9fa909f7c47d
Revises:
Create Date: 2025-04-12 01:44:47.801579

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9fa909f7c47d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("bookmarks", sa.ARRAY(sa.Integer()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
