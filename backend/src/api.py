from uuid import UUID

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi_users import FastAPIUsers
from starlette_csrf import CSRFMiddleware

from models.user import User
from routers import aggregations as aggregations_router
from routers import csrftoken
from routers import organisations as organisations_router
from routers import register as register_router
from routers import statistics as statistics_router
from routers import users as users_router
from routers import invitations as invitations_router
from routers import variables as variables_router
from security import users
from security.schemas import UserOut
from settings import settings

app = FastAPI()


def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


app = FastAPI(generate_unique_id_function=custom_generate_unique_id)


fastapi_users = FastAPIUsers[User, UUID](
    users.get_user_manager,
    [users.auth_backend],
)

app.add_middleware(
    CSRFMiddleware,
    secret=settings.csrf.secret,
    header_name=settings.csrf.header_name,
    cookie_name=settings.csrf.cookie_name,
    cookie_samesite=settings.csrf.cookie_samesite,
    cookie_secure=settings.csrf.cookie_secure,
    cookie_domain=settings.csrf.cookie_domain,
    exempt_urls=settings.csrf.exempt_urls,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

app.include_router(router=csrftoken.router, prefix="/csrf", tags=["/csrf"])

app.include_router(
    fastapi_users.get_auth_router(users.auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    register_router.router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserOut),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    users_router.router,
    prefix="/users",
    tags=["users"],
)

app.include_router(
    organisations_router.router,
    prefix="/organisations",
    tags=["organisations"],
)

app.include_router(
    variables_router.router,
    prefix="/variables",
    tags=["variables"],
)

app.include_router(
    invitations_router.router,
    prefix="/invitations",
    tags=["invitations"],
)

app.include_router(
    statistics_router.router,
    prefix="/statistics",
    tags=["statistics"],
)

app.include_router(
    aggregations_router.router,
    prefix="/aggregations",
    tags=["aggregations"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
