"""empty message

Revision ID: 0f916b2ffbe5
Revises: d165e2130a6c
Create Date: 2023-03-10 16:54:53.729181

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = '0f916b2ffbe5'
down_revision = 'd165e2130a6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seeds', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seeds', 'created_at')
    # ### end Alembic commands ###
