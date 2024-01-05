"""initial

Revision ID: 1fb793ed3b6c
Revises: 244947adc435
Create Date: 2023-12-25 19:04:17.657760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fb793ed3b6c'
down_revision: Union[str, None] = '244947adc435'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_bought_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', 'user_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_bought_products')
    # ### end Alembic commands ###
