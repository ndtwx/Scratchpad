"""empty message

Revision ID: e91042ba7a62
Revises: 2981f366d55f
Create Date: 2023-07-24 19:19:18.811228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e91042ba7a62'
down_revision = '2981f366d55f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('commenter_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['commenter_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('commenter_id')

    # ### end Alembic commands ###
