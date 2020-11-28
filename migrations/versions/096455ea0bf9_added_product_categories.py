"""Added product categories

Revision ID: 096455ea0bf9
Revises: f5cdc7a19abd
Create Date: 2020-11-27 17:44:06.898376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '096455ea0bf9'
down_revision = 'f5cdc7a19abd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'])
    op.drop_column('product', 'category')
    op.alter_column('user', 'password',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('product', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'category_id')
    op.drop_table('category')
    # ### end Alembic commands ###