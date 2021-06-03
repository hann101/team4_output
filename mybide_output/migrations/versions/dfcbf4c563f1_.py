"""empty message

Revision ID: dfcbf4c563f1
Revises: 73312326b620
Create Date: 2021-05-13 23:06:45.969255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfcbf4c563f1'
down_revision = '73312326b620'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('level', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'level')
    # ### end Alembic commands ###
