"""new migrattion

Revision ID: 08ddc74bbed5
Revises: 36e9f0177540
Create Date: 2022-05-29 15:38:09.263477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08ddc74bbed5'
down_revision = '36e9f0177540'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('total_deposit', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'total_deposit')
    # ### end Alembic commands ###
