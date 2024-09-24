from jinja2 import Environment, FileSystemLoader
from providers.scaleway.client import ScalewayClient
from providers.scaleway.transactional_email import SenderInformation
from settings import settings


async def send_email_template(
    email_template: str, sender: str, recipient: str, subject: str, **kwargs
) -> None:
    client = ScalewayClient(
        api_token=settings.scaleway.api_token,
        project_id=settings.scaleway.project_id,
    )
    file_loader = FileSystemLoader("./utils/email_templates")
    env = Environment(loader=file_loader)

    template = env.get_template(email_template)

    email = template.render(**kwargs)

    # prevent sending email in local environment, print email instead
    if settings.environment.environment.upper() == "LOCAL":
        print(email)

    # send email in development and production environment
    if settings.environment.environment.upper() in ["DEVELOPMENT", "PRODUCTION"]:
        await client.TransactionalEmail.send_email(
            sender=SenderInformation(email=sender, name="Quick-Check Bauantrag"),
            recipients=[
                SenderInformation(email=recipient),
            ],
            subject=subject,
            html=email,
        )
