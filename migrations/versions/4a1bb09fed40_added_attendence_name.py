"""Added Attendence>name

Revision ID: 4a1bb09fed40
Revises: c845117207ce
Create Date: 2024-04-22 16:36:58.981632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1bb09fed40'
down_revision = 'c845117207ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))
        batch_op.alter_column('date',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee_attendance', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DateTime(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.drop_column('name')

    # ### end Alembic commands ###