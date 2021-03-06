"""Remove unique value from game titles.

Revision ID: 6e93e182de1d
Revises: abba5c0d41a0
Create Date: 2020-04-13 14:54:42.460579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e93e182de1d'
down_revision = 'abba5c0d41a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_game_title', table_name='game')
    op.create_index(op.f('ix_game_title'), 'game', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_title'), table_name='game')
    op.create_index('ix_game_title', 'game', ['title'], unique=True)
    # ### end Alembic commands ###
