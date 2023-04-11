"""create purchase table

Revision ID: 8b61da465b3b
Revises: 427fab048398
Create Date: 2023-04-11 20:09:14.352231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b61da465b3b'
down_revision = '427fab048398'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchase",
        sa.Column("Id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("Price", sa.Integer, nullable=False),
        sa.Column("BuyType", sa.VARCHAR(30), nullable=False),
        sa.Column("BuyDate", sa.Date, nullable=False),
        sa.Column("FamilyId", sa.Integer, nullable=False),
        sa.Column("MemberId", sa.VARCHAR(30), nullable=False)
    )

    op.create_foreign_key("purchase_family_fk", "purchase", "family", ["FamilyId"], ["Id"])
    op.create_foreign_key("purchase_member_fk", "purchase", "familymember", ["MemberId"], ["TelegramId"])



def downgrade() -> None:
    op.drop_table("purchase")
