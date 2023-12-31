"""delete role column

Revision ID: 39d0ca8c9c64
Revises: d2ebf4335bfa
Create Date: 2023-07-03 18:53:18.870397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39d0ca8c9c64'
down_revision = 'd2ebf4335bfa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.TEXT(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
