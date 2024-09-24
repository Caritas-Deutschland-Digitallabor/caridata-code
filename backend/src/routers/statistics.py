# add post endpoint that posts data to the statistics table

import logging
import uuid
from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_async_session
from models.statistics import Statistics

router = APIRouter()

logger = logging.getLogger(__name__)


# Todo add better typing
class StatisticsIn(BaseModel):
    aggregation_id: str
    organisation_id: str
    period_level: str
    period: date
    value: int
    upload_id: str
    grouping_category_1_value: Optional[str] = None
    grouping_category_2_value: Optional[str] = None
    grouping_variable_1_id: Optional[str] = None
    grouping_variable_2_id: Optional[str] = None


@router.post("/", name="add_statistics")
async def add_statistics(
    request: list[StatisticsIn],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    stmt = insert(Statistics).values(
        [
            {
                "id": str(uuid.uuid4()),
                "aggregation_id": r.aggregation_id,
                "organisation_id": r.organisation_id,
                "period_level": r.period_level,
                "period": r.period,
                "value": r.value,
                "upload_id": r.upload_id,
                "grouping_category_1_value": r.grouping_category_1_value,
                "grouping_category_2_value": r.grouping_category_2_value,
                "grouping_variable_1_id": r.grouping_variable_1_id,
                "grouping_variable_2_id": r.grouping_variable_2_id,
            }
            for r in request
        ]
    )
    await db_session.execute(stmt)

    return request
