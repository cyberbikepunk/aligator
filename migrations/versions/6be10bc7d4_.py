"""empty message

Revision ID: 6be10bc7d4
Revises: 3a5ccb3c7e8
Create Date: 2015-09-18 15:10:01.521763

"""

# revision identifiers, used by Alembic.
revision = '6be10bc7d4'
down_revision = '3a5ccb3c7e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('test', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'test')
    ### end Alembic commands ###