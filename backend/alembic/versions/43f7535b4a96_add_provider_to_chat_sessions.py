"""add provider to chat sessions

Revision ID: 43f7535b4a96
Revises: 2de954d81cb7
Create Date: 2026-08-01 09:23:22.123471
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "43f7535b4a96"
down_revision: Union[str, Sequence[str], None] = "853f016a1c38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the column with a temporary default
    op.add_column(
        "chat_sessions",
        sa.Column(
            "provider",
            sa.String(length=50),
            nullable=False,
            server_default="ollama",
        ),
    )

    # Remove the default after existing rows are populated
    op.alter_column(
        "chat_sessions",
        "provider",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "chat_sessions",
        "provider",
    )