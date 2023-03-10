"""empty message

Revision ID: 4fee52b11858
Revises: 61b915490808
Create Date: 2023-03-10 15:57:04.879001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fee52b11858'
down_revision = '61b915490808'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seeds')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seeds',
    sa.Column('id', sa.CHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('is_executed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='seeds_pkey')
    )
    # ### end Alembic commands ###
