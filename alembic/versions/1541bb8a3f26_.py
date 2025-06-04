"""empty message

Revision ID: 1541bb8a3f26
Revises:
Create Date: 2024-07-22 18:50:19.621125

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1541bb8a3f26"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL UNIQUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            tz_region VARCHAR(50),
            tz_offset VARCHAR(10),
            longitude REAL,
            latitude REAL,
            language VARCHAR(10),
            role VARCHAR(30),
            is_alive BOOLEAN NOT NULL,
            banned BOOLEAN NOT NULL
        );
    """)


def downgrade() -> None:
    op.execute("""DROP TABLE users;""")
