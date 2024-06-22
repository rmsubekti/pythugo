"""empty message

Revision ID: 95e0c5ece9e4
Revises: 19ce2266e0d9
Create Date: 2024-06-22 03:34:48.904878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95e0c5ece9e4'
down_revision = '19ce2266e0d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('avatar_url', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('repo', sa.String(length=150), nullable=False),
    sa.Column('path', sa.String(length=100), nullable=False),
    sa.Column('ssh', sa.String(length=100), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blog_author',
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], ),
    sa.PrimaryKeyConstraint('author_id', 'blog_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_author')
    op.drop_table('blog')
    op.drop_table('author')
    # ### end Alembic commands ###
