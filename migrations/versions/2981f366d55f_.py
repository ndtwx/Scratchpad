"""empty message

Revision ID: 2981f366d55f
Revises: 68eb4b0b8800
Create Date: 2023-07-24 19:09:56.812960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2981f366d55f'
down_revision = '68eb4b0b8800'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
