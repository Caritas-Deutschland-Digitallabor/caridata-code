from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Variable(Base):
    __tablename__ = "variables"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    value_from: Mapped[str] = mapped_column(String, nullable=True)
    value_to: Mapped[str] = mapped_column(String, nullable=True)
    mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False)
    technical_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False)
    file_position: Mapped[int] = mapped_column(Integer, nullable=True)
    deprecated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    missing: Mapped[bool] = mapped_column(String, nullable=True, default=False)
    categories = relationship("Category", back_populates="variable")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    variable_id: Mapped[str] = mapped_column(
        String, ForeignKey("variables.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    deprecated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    variable = relationship("Variable", back_populates="categories")
