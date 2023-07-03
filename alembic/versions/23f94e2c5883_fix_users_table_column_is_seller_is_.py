"""fix Users table column is_Seller -> is_seller

Revision ID: 23f94e2c5883
Revises: 000ef7aaab14
Create Date: 2023-07-04 00:38:43.246541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23f94e2c5883'
down_revision = '000ef7aaab14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_seller', sa.Boolean(), server_default='FALSE', nullable=True))
    op.drop_column('users', 'is_Seller')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_Seller', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True))
    op.drop_column('users', 'is_seller')
    # ### end Alembic commands ###
