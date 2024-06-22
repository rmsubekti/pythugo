"""empty message

Revision ID: 4f89e33927e9
Revises: 17a6ed9e6618
Create Date: 2024-06-22 04:01:50.394804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f89e33927e9'
down_revision = '17a6ed9e6618'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('github_token', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('github_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=40), nullable=False))

    # ### end Alembic commands ###
