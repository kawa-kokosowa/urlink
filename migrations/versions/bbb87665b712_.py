"""empty message

Revision ID: bbb87665b712
Revises: a77719286100
Create Date: 2016-10-03 14:47:08.668969

"""

# revision identifiers, used by Alembic.
revision = 'bbb87665b712'
down_revision = 'a77719286100'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('urls', sa.Column('content_type', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('urls', 'content_type')
    ### end Alembic commands ###