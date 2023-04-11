"""create family table

Revision ID: b4ff6c577962
Revises: 
Create Date: 2023-04-11 19:51:08.007836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4ff6c577962'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "family",
        sa.Column("Id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("Login", sa.VARCHAR(30), unique=True, nullable=False),
        sa.Column("Pass", sa.VARCHAR(30), nullable=False),
        sa.Column("FamilyName", sa.VARCHAR(30), nullable=False)


    )


def downgrade() -> None:
    op.drop_table("family")
