"""added path

Revision ID: 9c9ea33d0cb2
Revises: 2e2f03543848
Create Date: 2025-04-17 11:53:18.520261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c9ea33d0cb2'
down_revision: Union[str, None] = '2e2f03543848'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('path', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'path')
    # ### end Alembic commands ###
