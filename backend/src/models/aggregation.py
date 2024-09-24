from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Aggregation(Base):
    __tablename__ = "aggregations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    schema_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("aggregation_schemas.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    aggregation_variable_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("variables.id", ondelete="CASCADE"),
        nullable=False,
    )
    group_variable_1_id: Mapped[str] = mapped_column(
        String, ForeignKey("variables.id", ondelete="CASCADE"), nullable=True
    )
    group_variable_2_id: Mapped[str] = mapped_column(
        String, ForeignKey("variables.id", ondelete="CASCADE"), nullable=True
    )
    source: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    deprecated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    schema: Mapped["AggregationSchema"] = relationship(
        "AggregationSchema", back_populates="aggregations"
    )


class AggregationSchema(Base):
    __tablename__ = "aggregation_schemas"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    filter: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_distinct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    aggregation_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    deprecated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    aggregations: Mapped[list["Aggregation"]] = relationship(
        "Aggregation", back_populates="schema"
    )
