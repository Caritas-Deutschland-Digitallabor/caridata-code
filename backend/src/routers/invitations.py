from datetime import datetime, timezone, timedelta, time
from typing import Annotated, Sequence
from uuid import UUID, uuid4
from secrets import token_urlsafe

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Path,
)
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, EmailStr, AwareDatetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from security import users
from database.session import get_async_session
from models.user import User
from models.organisation import Organisation, Invitation
from settings import settings
from utils.send_email import send_email_template


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


class InvitationDB(BaseModel):
    id: UUID = uuid4()
    organisation_id: int
    email: EmailStr
    token: str
    created_at: datetime = datetime.now(timezone.utc)
    expires_at: datetime = datetime.combine(
        datetime.now(), time.max, timezone.utc
    ) + timedelta(weeks=8)


class InvitationOut(BaseModel):
    id: UUID
    organisation_id: int
    email: EmailStr
    token: str
    created_at: AwareDatetime
    expires_at: AwareDatetime

    model_config = {"from_attributes": True}


class CheckTokenOut(BaseModel):
    organisation_id: int


async def get_organisation_by_id_dependency(
    organisation_id: Annotated[int, Path(..., description="ID der Organisation")],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organisation:
    """
    Get an organisation by its ID.

    Args:
        organisation_id (int): Organisation ID
        db_session (AsyncSession): AsyncSession instance
    """
    organisation = await db_session.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organisation nicht vorhanden"
        )
    return organisation


async def generate_unique_invitation_token(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    """
    Generate a random invitation token and check if it is unique in the database.

    Args:
        db_session (AsyncSession): AsyncSession instance
    """
    while True:
        token = token_urlsafe(64)
        select_stmt = select(Invitation).where(Invitation.token == token)
        result = await db_session.execute(select_stmt)
        invitation = result.scalar_one_or_none()
        if not invitation:
            return token


async def send_email(
    invitation: Annotated[Invitation, ...], organisation: Annotated[Organisation, ...]
) -> None:
    """
    Send an email to the recipient of the invitation.

    Args:
        invitation (Invitation): Invitation instance
        organisation (Organisation): Organisation instance
    """
    magic_link = f"{settings.email.domain}upload?token={invitation.token}"
    expiration_date = invitation.expires_at.strftime("%d.%m.%Y")
    await send_email_template(
        email_template="user_invitation_data_upload_template.html",
        sender=settings.email.sender,
        recipient=invitation.email,
        subject="Einladung zum Upload",
        organisation_name=organisation.name,
        expiration_date=expiration_date,
        magic_link=magic_link,
    )


@router.post(
    "/send/{organisation_id}",
    name="send_invitation",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def send_invitation(
    organisation: Annotated[Organisation, Depends(get_organisation_by_id_dependency)],
    token: Annotated[str, Depends(generate_unique_invitation_token)],
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """
    Send an invitation to a representative of an organisation to upload data.

    Args:
        organisation (Organisation): Organisation instance
        token (str): Invitation token
        db_session (AsyncSession): AsyncSession instance
    """
    if not organisation.invitation_email and not organisation.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organisation hat keine E-Mail-Adresse",
        )
    # Use the invitation email address if available, otherwise use the organisation email address
    email = (
        organisation.invitation_email
        if organisation.invitation_email
        else organisation.email
    )
    # Check if the organisation has already sent an invitation
    lastest_invitation = (
        organisation.invitations[0] if organisation.invitations else None
    )
    # Check if there is already an active invitation for this email address and organisation
    # If so, resend the email
    if (
        lastest_invitation
        and lastest_invitation.expires_at > datetime.now(timezone.utc)
        and lastest_invitation.email == email
    ):
        invitation = lastest_invitation
        await send_email(invitation, organisation)
        return
    # Create a new invitation
    # Check if there is already an active invitation for this organisation
    # but with a different email address
    # If so, deactivate the old invitation and create a new one
    # Otherwise, just create a new invitation
    # In both cases, send the email
    invitation = Invitation(
        **InvitationDB(
            id=uuid4(),  # noqa
            organisation_id=organisation.id,
            email=email,
            token=token,
        ).model_dump()
    )
    if (
        lastest_invitation
        and lastest_invitation.expires_at > datetime.now(timezone.utc)
        and lastest_invitation.email != email
    ):
        lastest_invitation.expires_at = datetime.now(timezone.utc)

    await send_email(invitation, organisation)
    db_session.add(invitation)


@router.get(
    "/",
    name="list_invitations",
    response_model=list[InvitationOut],
    dependencies=[Depends(get_current_active_verified_superuser)],
)
async def list_invitations(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Sequence[Invitation]:
    """
    List all invitations.

    Args:
        db_session (AsyncSession): AsyncSession instance
    """
    select_stmt = select(Invitation)
    result = await db_session.execute(select_stmt)
    invitations = result.scalars().all()

    if not invitations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Keine Einladungen vorhanden"
        )

    return invitations


@router.get(
    "/check-token/{token}",
    name="check_invitation_token",
    response_model=CheckTokenOut,
    status_code=status.HTTP_200_OK,
)
async def check_invitation_token(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Path(..., description="Einladungs-Token")],
) -> CheckTokenOut:
    """
    Check if an invitation token is valid.

    Args:
        db_session (AsyncSession): AsyncSession instance
        token (str): Invitation token
    """
    select_stmt = select(Invitation).where(Invitation.token == token)
    result = await db_session.execute(select_stmt)
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keine Einladung für diesen Token vorhanden",
        )
    if invitation.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Einladung ist abgelaufen",
        )

    response = CheckTokenOut(organisation_id=invitation.organisation_id)

    return response
