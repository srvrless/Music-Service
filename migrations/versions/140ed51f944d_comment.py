"""comment

Revision ID: 140ed51f944d
Revises: 7fdf29f4f14e
Create Date: 2023-03-04 13:51:15.819551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '140ed51f944d'
down_revision = '7fdf29f4f14e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('liked_song', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.drop_column('liked_song', 'is_liked')
    op.add_column('song', sa.Column('img_file', sa.String(), nullable=True))
    op.alter_column('song', 'song_file',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('song_song_file_key', 'song', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('song_song_file_key', 'song', ['song_file'])
    op.alter_column('song', 'song_file',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('song', 'img_file')
    op.add_column('liked_song', sa.Column('is_liked', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('liked_song', 'created_at')
    # ### end Alembic commands ###
