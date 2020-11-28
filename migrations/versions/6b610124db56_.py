"""empty message

Revision ID: 6b610124db56
Revises: 096455ea0bf9
Create Date: 2020-11-27 19:05:42.046352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b610124db56'
down_revision = '096455ea0bf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('store_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('store', sa.Column('email', sa.String(), nullable=True))
    op.add_column('store', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store', 'phone_number')
    op.drop_column('store', 'email')
    op.drop_table('store_category')
    # ### end Alembic commands ###