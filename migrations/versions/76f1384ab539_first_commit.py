"""First commit

Revision ID: 76f1384ab539
Revises: 
Create Date: 2024-03-20 16:55:16.077614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '76f1384ab539'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.Enum('private', 'channel', 'group', 'supergroup', name='typeofchat'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__chats')),
    sa.UniqueConstraint('tg_id', name=op.f('uq__chats__tg_id'))
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('is_bot', sa.Boolean(), nullable=False),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    sa.UniqueConstraint('tg_id', name=op.f('uq__users__tg_id'))
    )
    op.create_table('advertisments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('ad_type', sa.Enum('take', 'give', name='typeofad'), nullable=False),
    sa.Column('delivery_type', sa.Enum('meeting', 'mail', 'courier', name='typeofdelivery'), nullable=False),
    sa.Column('constant_need', sa.Boolean(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('additional_text', sa.String(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__advertisments__user_id__users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__advertisments'))
    )
    op.create_table('drugs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['advertisments.id'], name=op.f('fk__drugs__ad_id__advertisments'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__drugs'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drugs')
    op.drop_table('advertisments')
    op.drop_table('users')
    op.drop_table('chats')
    # ### end Alembic commands ###
