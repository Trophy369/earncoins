"""new migration

Revision ID: 6bf425457271
Revises: 95d01989ed5e
Create Date: 2022-05-25 06:44:00.714887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bf425457271'
down_revision = '95d01989ed5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('transaction_imgs', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'transaction_imgs')
    # ### end Alembic commands ###
