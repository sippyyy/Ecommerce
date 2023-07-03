"""Add FK and relationship for Products table

Revision ID: 5c935fbad435
Revises: 9563e83bf2ef
Create Date: 2023-07-04 00:25:30.839456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c935fbad435'
down_revision = '9563e83bf2ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'products', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'owner_id')
    # ### end Alembic commands ###