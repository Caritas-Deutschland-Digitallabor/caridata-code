from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    invitation_email: Mapped[str] = mapped_column(String, nullable=True)
    invitations: Mapped[list["Invitation"]] = relationship(
        "Invitation",
        lazy="selectin",
        order_by="desc(Invitation.expires_at), desc(Invitation.created_at)",
    )
    deprecated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    organisation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organisations.id", ondelete="SET NULL"), nullable=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
