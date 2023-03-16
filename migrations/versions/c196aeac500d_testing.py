"""testing

Revision ID: c196aeac500d
Revises: b8782899377f
Create Date: 2023-03-16 19:16:04.171966

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c196aeac500d'
down_revision = 'b8782899377f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(255), nullable=True))
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###
