from datetime import datetime, timezone
import logging
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)
from fastapi_users import FastAPIUsers
import httpx
from pydantic import BaseModel, EmailStr, ValidationError, AwareDatetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from security import users
from database.session import get_async_session
from models.user import User
from models.organisation import Organisation
from settings import settings

logger = logging.getLogger(__name__)

router = APIRouter()

fastapi_users = FastAPIUsers[User, UUID](
    users.fastapi_users.get_user_manager,
    [users.auth_backend],
)

get_current_active_user = fastapi_users.authenticator.current_user(
    active=True, verified=False
)

get_current_active_verified_user = fastapi_users.authenticator.current_user(
    active=True, verified=True
)

get_current_active_verified_superuser = fastapi_users.authenticator.current_user(
    active=True, verified=True, superuser=True
)


class InvitationOut(BaseModel):
    id: UUID
    organisation_id: int
    email: EmailStr
    token: str
    created_at: AwareDatetime
    expires_at: AwareDatetime

    model_config = {"from_attributes": True}


class OrganisationIn(BaseModel):
    id: int
    name: str | None = None
    email: EmailStr | None = None


class OrganisationOut(BaseModel):
    id: int
    name: str | None = None
    email: EmailStr | None = None
    invitation_email: EmailStr | None = None
    invitations: list[InvitationOut] | None = None
    created_at: AwareDatetime
    updated_at: AwareDatetime | None = None
    deprecated_at: AwareDatetime | None = None

    model_config = {"from_attributes": True}


async def get_caritas_api_response(path: str) -> dict:
    url = f"{settings.caritas.api_uri}{path}"
    auth = (
        settings.caritas.api_basic_auth_username,
        settings.caritas.api_basic_auth_password,
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            auth=auth,
        )
        response.raise_for_status()
        return response.json()


async def get_organisation_by_id_dependency(
    organisation_id: Annotated[int, Path(..., description="ID der Organisation")],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organisation:
    select_stmt = select(Organisation).filter(Organisation.id == organisation_id)
    result = await db_session.execute(select_stmt)
    organisation = result.scalars().first()
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organisation nicht vorhanden"
        )
    return organisation


@router.get(
    "/",
    name="list_organisations",
    response_model=list[OrganisationOut],
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def list_organisations(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    all: Annotated[
        bool, Query(..., description="Auch gelöschte Organisationen anzeigen")
    ] = False,
) -> Sequence[Organisation]:
    select_stmt = select(Organisation)
    if not all:
        select_stmt = select_stmt.filter(Organisation.deprecated_at.is_(None))
    select_stmt = select_stmt.order_by(Organisation.id)
    result = await db_session.execute(select_stmt)
    organisations = result.scalars().all()
    return organisations


@router.get(
    "/{organisation_id}/",
    name="get_organisation_by_id",
    response_model=OrganisationOut,
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def get_organisation_by_id(
    organisation: Annotated[Organisation, Depends(get_organisation_by_id_dependency)],
) -> Organisation:
    return organisation


@router.patch(
    "/synchronisieren/",
    name="synchronize_organisations",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def synchronize_organisations(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    api_response = await get_caritas_api_response(
        f"/categories/{settings.caritas.api_category}/contents?pagesize=10000"
    )
    organisations = []
    for organisation_data in api_response["Items"]:
        # Use email if it exists, otherwise use None
        email = organisation_data["Email"] if organisation_data["Email"] else None
        # Use the first email address if multiple are present
        # and remove whitespaces and convert to lowercase
        if email:
            email = email.split(",")[0]
            email = email.replace(" ", "")
            email = email.lower()

        try:
            # Validate organisation data
            organisation = OrganisationIn(
                id=int(organisation_data["Number"]),
                name=organisation_data["Title"],
                email=email,
            )
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            # Remove email from organisation if it is invalid
            if email in e.errors():
                organisation.email = None
        # Append organisation to list as dict to avoid issues with insertion
        organisations.append(organisation.model_dump())
    # Remove duplicates from organisations list
    organisations = [dict(t) for t in {tuple(d.items()) for d in organisations}]

    # Deprecate organisations that do not have their ID present in the API response
    deprecation_stmt = (
        update(Organisation)
        .where(
            Organisation.id.notin_([org["id"] for org in organisations]),
            Organisation.deprecated_at.is_(None),
        )
        .values(deprecated_at=datetime.now(timezone.utc))
    )

    await db_session.execute(deprecation_stmt)

    # Insert or update organisations
    # on_conflict_do_update updates the email, name and updated_at of the organisation
    # and sets the deprecated_at to NULL in case of a previously deprecated organisation.
    # If the organisation is not present in the database, it will be inserted
    upsert_stmt = insert(Organisation).values(organisations)
    upsert_stmt = upsert_stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "updated_at": datetime.now(timezone.utc),
            "email": upsert_stmt.excluded.email,
            "name": upsert_stmt.excluded.name,
            "deprecated_at": None,
        },
    )

    await db_session.execute(upsert_stmt)


@router.patch(
    "/{organisation_id}/invitation-email/",
    name="upsert_organisation_invitation_email",
    response_model=OrganisationOut,
    status_code=status.HTTP_200_OK,
    # TODO: Discuss if this should be a superuser or a just a verified user
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def upsert_organisation_invitation_email(
    organisation: Annotated[Organisation, Depends(get_organisation_by_id_dependency)],
    email: Annotated[
        EmailStr,
        Body(..., description="E-Mail-Adresse für Einladungen"),
    ],
) -> Organisation:
    normalized_email = email.lower()
    organisation.invitation_email = normalized_email
    organisation.updated_at = datetime.now(timezone.utc)
    return organisation
