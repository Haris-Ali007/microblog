"""resolving error

Revision ID: 5c9e2855dde1
Revises: d9aedbc94964
Create Date: 2024-02-17 15:44:49.844879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c9e2855dde1'
down_revision = 'd9aedbc94964'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('about_me',
               existing_type=sa.VARCHAR(length=140),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('about_me',
               existing_type=sa.VARCHAR(length=140),
               nullable=False)

    # ### end Alembic commands ###
