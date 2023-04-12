"""create family member table

Revision ID: 427fab048398
Revises: b4ff6c577962
Create Date: 2023-04-11 20:03:17.023460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427fab048398'
down_revision = 'b4ff6c577962'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "familymember",
        sa.Column("Id", sa.INT, autoincrement=True, nullable=False, primary_key=True),
        sa.Column("UserName", sa.VARCHAR(30),  nullable=False),
        sa.Column("TelegramId", sa.VARCHAR(30), nullable=False, unique=True, primary_key=True),
        sa.Column("FamilyId", sa.Integer)

    )
    op.create_foreign_key("familymember_fk", "familymember", "family", ["FamilyId"], ["Id"])


def downgrade() -> None:
    op.drop_table("familymember")
