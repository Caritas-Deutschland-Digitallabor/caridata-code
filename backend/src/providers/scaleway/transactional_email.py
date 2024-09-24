import typing

from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from providers.scaleway.client import ScalewayClient


class SenderInformation(BaseModel):
    email: str
    name: str | None = None


class TransactionalEmailService:
    endpoint: str = "/transactional-email/v1alpha1/regions/fr-par/emails"

    def __init__(self, client: "ScalewayClient") -> None:
        self.client = client

    async def send_email(
        self,
        sender: SenderInformation,
        recipients: list[SenderInformation],
        subject: str,
        text: str = "",
        html: str = "",
        cc: list[str] = [],
        bcc: list[str] = [],
        attachments: list[str] = [],
        project_id: str | None = None,
    ):
        response = await self.client.client.post(
            self.endpoint,
            json={
                "from": sender.model_dump(),
                "to": [
                    recipient.model_dump(exclude_unset=True) for recipient in recipients
                ],
                "subject": subject,
                "text": text,
                "html": html,
                "cc": cc,
                "bcc": bcc,
                "attachments": attachments,
                "project_id": project_id if project_id else self.client.project_id,
            },
        )
        response.raise_for_status()
