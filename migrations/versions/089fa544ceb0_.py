"""empty message

Revision ID: 089fa544ceb0
Revises: 
Create Date: 2020-03-26 22:39:45.171471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '089fa544ceb0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('USER', sa.Column('image', sa.String(length=600), nullable=False))
    op.alter_column('details', 'users',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('details', 'users',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('USER', 'image')
    # ### end Alembic commands ###