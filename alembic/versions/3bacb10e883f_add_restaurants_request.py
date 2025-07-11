"""add restaurants.request

Revision ID: 3bacb10e883f
Revises: 
Create Date: 2025-07-04 11:19:18.826032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bacb10e883f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('request', sa.Enum('pending', 'accepted', 'rejected', name='restaurantrequest'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurants', 'request')
    # ### end Alembic commands ###
