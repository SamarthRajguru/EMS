"""Initial State

Revision ID: 70f7f690ccab
Revises: 
Create Date: 2024-04-17 13:09:13.758870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70f7f690ccab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_details', schema=None) as batch_op:
        batch_op.drop_column('paid_leaves_left')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paid_leaves_left', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###