import httpx
from providers.scaleway.transactional_email import TransactionalEmailService


class ScalewayAuth(httpx.Auth):
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def auth_flow(self, request):
        request.headers["X-Auth-Token"] = self.api_token
        yield request


class ScalewayClient:
    def __init__(
        self,
        *,
        api_token: str,
        project_id: str,
        base_url: str = "https://api.scaleway.com/",
    ) -> None:
        self.api_token = api_token
        self.project_id = project_id
        self.client = httpx.AsyncClient(
            base_url=base_url,
            auth=ScalewayAuth(api_token),
            timeout=60,
        )
        self.TransactionalEmail = TransactionalEmailService(self)
