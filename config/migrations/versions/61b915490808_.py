"""empty message

Revision ID: 61b915490808
Revises: c7926eb45447
Create Date: 2023-03-10 15:38:38.513724

"""
from alembic import op
import sqlalchemy as sa
import ormar

# revision identifiers, used by Alembic.
revision = "61b915490808"
down_revision = "c7926eb45447"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "seeds",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
        sa.Column("is_executed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("seeds")
    # ### end Alembic commands ###
