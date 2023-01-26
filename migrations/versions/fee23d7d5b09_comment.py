"""comment

Revision ID: fee23d7d5b09
Revises: b0ffb328f7ef
Create Date: 2023-01-26 02:46:47.387000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fee23d7d5b09'
down_revision = 'b0ffb328f7ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('songs',
                    sa.Column('song_id', postgresql.UUID(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('creator', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('is_liked', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('song_id', name='songs_pkey'),
                    sa.UniqueConstraint('name', name='songs_name_key')
                    )
    op.create_table('users',
                    sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False),
                    sa.Column('nickname', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('email_address', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
                    sa.UniqueConstraint('email_address', name='users_email_address_key'),
                    sa.UniqueConstraint('nickname', name='users_nickname_key')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('songs')
    # ### end Alembic commands ###