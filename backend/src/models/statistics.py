from datetime import date
from uuid import UUID

from sqlalchemy import Date, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    # aggregation_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("aggregations.id", ondelete="SET NULL"), nullable=True
    # ) # Todo: fix with foreign key when rest of backend is implemented
    aggregation_id: Mapped[int] = mapped_column(String, nullable=True)
    organisation_id: Mapped[str] = mapped_column(
        String, nullable=True
    )  # Todo: Make mandatory
    period_level: Mapped[date] = mapped_column(
        String, nullable=True
    )  # Todo: Make mandatory
    period: Mapped[int] = mapped_column(Date, nullable=True)  # Todo: Make mandatory
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_id: Mapped[str] = mapped_column(
        String, nullable=True
    )  # Todo: Implement this with upload table
    grouping_category_1_value: Mapped[str] = mapped_column(String, nullable=True)
    grouping_category_2_value: Mapped[str] = mapped_column(String, nullable=True)
    grouping_variable_1_id: Mapped[str] = mapped_column(String, nullable=True)
    grouping_variable_2_id: Mapped[str] = mapped_column(String, nullable=True)
