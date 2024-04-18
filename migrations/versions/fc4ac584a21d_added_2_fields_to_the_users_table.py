"""Added 2 fields to the users table

Revision ID: fc4ac584a21d
Revises: f9393b285a46
Create Date: 2024-04-15 03:25:32.478503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc4ac584a21d'
down_revision: Union[str, None] = 'f9393b285a46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_banned', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_banned')
    # ### end Alembic commands ###