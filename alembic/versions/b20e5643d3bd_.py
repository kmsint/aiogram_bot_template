"""empty message

Revision ID: b20e5643d3bd
Revises: 1541bb8a3f26
Create Date: 2024-07-23 01:42:36.705479

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b20e5643d3bd"
down_revision: Union[str, None] = "1541bb8a3f26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
