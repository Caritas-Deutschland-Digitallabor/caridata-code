import logging
from datetime import datetime
from typing import Annotated, Literal, Sequence

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
from models.variable import Variable

logger = logging.getLogger(__name__)

router = APIRouter()


class CategoryOut(BaseModel):
    name: str | None = None
    value: str


class SchemaOut(BaseModel):
    id: str
    name: str
    source: str
    text: str
    type: str
    value_from: str | None = None
    value_to: str | None = None
    technical_mandatory: bool
    mandatory: bool
    file_position: int
    missing: str | None = None
    created_at: datetime
    deprecated_at: datetime | None = None
    categories: list[CategoryOut] | None = None


source_types = Literal["sbkont", "sbkern1", "stelle", "sbveran", "sbkern2"]


@router.get(
    "/",
    name="list_variables",
    response_model=list[SchemaOut],
)
async def list_variables(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    variable_name: Annotated[
        str | None, Query(..., description="Name of the variable")
    ] = None,
    source: source_types = Query(None, description="Source of the variable"),
) -> Sequence[SchemaOut]:  # type: ignore
    stmt = select(Variable).options(selectinload(Variable.categories))
    if variable_name:
        stmt = stmt.where(Variable.name == variable_name)
    if source:
        ## TODO: Delete this work around when parsing is fixed
        stmt = stmt.where(Variable.source == source)
    result = await db_session.execute(stmt)
    variables = result.scalars().all()
    schemas = []
    for variable in variables:
        var_dict = {
            "id": variable.id,
            "name": variable.name,
            "source": variable.source,
            "text": variable.text,
            "type": variable.type,
            "value_from": variable.value_from,
            "value_to": variable.value_to,
            "mandatory": variable.mandatory,
            "technical_mandatory": variable.technical_mandatory,
            "file_position": variable.file_position,
            "missing": variable.missing,
            "created_at": variable.created_at,
            "deprecated_at": variable.deprecated_at,
            "categories": [
                {"name": cat.name, "value": cat.value} for cat in variable.categories
            ]
            if variable.categories
            else None,
        }
        schemas.append(SchemaOut(**var_dict))  # type: ignore[arg-type]
    return schemas
