import logging
from typing import Annotated, Literal, Sequence
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.session import get_async_session
from models.aggregation import Aggregation

logger = logging.getLogger(__name__)

router = APIRouter()


class AggregationFilterConditions(BaseModel):
    field: str
    value: str | int | float
    condition: Literal["=", "!=", ">", "<", ">=", "<=", "IS NOT", "IS"]


class AggregationFilters(BaseModel):
    operator: Literal["AND", "OR"] | None = None
    conditions: list[AggregationFilterConditions]


class AggregationOut(BaseModel):
    id: str
    name: str
    schema_id: UUID
    source: str
    aggregation_variable_id: str
    aggregation_variable_name: str
    description_aggregation: str | None = None
    description_schema: str | None = None
    grouping_variable_1_id: str | None = None
    grouping_variable_2_id: str | None = None
    is_distinct: bool
    aggregation_type: str | None = None
    filter: AggregationFilters | None = None


source_types = Literal["sbkont", "sbkern1", "stelle", "sbveran", "sbkern2"]


@router.get(
    "/",
    name="list_aggregations",
    response_model=list[AggregationOut],
)
async def list_variables(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    source: source_types = Query(None, description="Source of the variable"),
    schema_id: Annotated[str | None, Query(..., description="Id of the schema")] = None,
) -> Sequence[AggregationOut]:  # type: ignore
    stmt = select(Aggregation).options(selectinload(Aggregation.schema))
    if source:
        stmt = stmt.filter(Aggregation.source == source)
    if schema_id:
        stmt = stmt.filter(Aggregation.schema_id == schema_id)
    result = await db_session.execute(stmt)

    aggregations = result.scalars().all()

    aggregation_schemas = []

    for aggregation in aggregations:
        schema_dict = {
            "id": aggregation.id,
            "name": aggregation.name,
            "schema_id": aggregation.schema_id,
            "source": aggregation.source,
            "description_aggregation": aggregation.description,
            "description_schema": aggregation.schema.description,
            "aggregation_variable_id": aggregation.aggregation_variable_id,
            "aggregation_variable_name": aggregation.aggregation_variable_id.split("_")[
                0
            ],
            "grouping_variable_1_id": aggregation.group_variable_1_id,
            "grouping_variable_2_id": aggregation.group_variable_2_id,
            "is_distinct": aggregation.schema.is_distinct,
            "aggregation_type": aggregation.schema.aggregation_type,
            "filter": aggregation.schema.filter,
        }
        aggregation_schemas.append(AggregationOut(**schema_dict))  # type: ignore

    return aggregation_schemas
