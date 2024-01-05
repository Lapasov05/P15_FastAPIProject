"""second migrations

Revision ID: 244947adc435
Revises: 1ea46c44378b
Create Date: 2023-12-25 18:59:48.173386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '244947adc435'
down_revision: Union[str, None] = '1ea46c44378b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
