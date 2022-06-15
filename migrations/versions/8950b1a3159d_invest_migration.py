"""invest migration

Revision ID: 8950b1a3159d
Revises: b745ebf3e7e6
Create Date: 2022-06-05 21:40:14.116390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8950b1a3159d'
down_revision = 'b745ebf3e7e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'referrer', 'users', ['ref_id'], ['id'])
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'referrer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('referrer', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'users', 'referrer', ['referrer'], ['id'])
    op.drop_constraint(None, 'referrer', type_='foreignkey')
    # ### end Alembic commands ###
