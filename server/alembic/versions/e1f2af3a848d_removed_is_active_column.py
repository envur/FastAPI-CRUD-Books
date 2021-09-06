"""Removed is_active column

Revision ID: e1f2af3a848d
Revises: 0682f285ddce
Create Date: 2021-09-06 09:23:48.598141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1f2af3a848d'
down_revision = '0682f285ddce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###