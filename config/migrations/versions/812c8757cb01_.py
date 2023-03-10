"""empty message

Revision ID: 812c8757cb01
Revises: 1273f06aaece
Create Date: 2023-03-13 16:10:46.033586

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = "812c8757cb01"
down_revision = "1273f06aaece"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("test")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "test",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("test", sa.VARCHAR(length=10), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="test_pkey"),
    )
    # ### end Alembic commands ###
