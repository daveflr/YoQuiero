"""Test Shopping cart 2.0

Revision ID: 114d3bc68b22
Revises: 1579ebe6049e
Create Date: 2020-07-12 14:38:41.824292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '114d3bc68b22'
down_revision = '1579ebe6049e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('shopping_cart')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopping_cart',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='shopping_cart_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='shopping_cart_pkey')
    )
    op.drop_table('cart_item')
    # ### end Alembic commands ###