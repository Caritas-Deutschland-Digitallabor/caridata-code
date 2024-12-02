"""organisation

Revision ID: 0002
Revises: 0001
Create Date: 2024-07-15 14:09:48.185267

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organisations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("invitation_email", sa.String(), nullable=True),
        sa.Column("deprecated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "invitations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organisation_id", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"], ["organisations.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("invitations")
    op.drop_table("organisations")
    # ### end Alembic commands ###
