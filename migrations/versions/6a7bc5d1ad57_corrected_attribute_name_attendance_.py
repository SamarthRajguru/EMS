"""Corrected Attribute name Attendance>Present

Revision ID: 6a7bc5d1ad57
Revises: 279a00ddf20e
Create Date: 2024-04-19 14:36:12.575509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a7bc5d1ad57'
down_revision = '279a00ddf20e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('present', sa.Boolean(), nullable=True))
        batch_op.drop_column('pesent')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pesent', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('present')

    # ### end Alembic commands ###
