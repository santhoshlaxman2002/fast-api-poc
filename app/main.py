import uuid
import logging
from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI, Request
from app.routers import users,products,auth,files
from app.core.exceptions import AppException
from app.core.exception_handler import app_exception_handler, validation_exception_handler, generic_exception_handler, database_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

app = FastAPI()


def _add_swagger_file_format(value: Any) -> None:
    """Add Swagger UI's file-input hint to Pydantic's OpenAPI 3.1 file schema."""
    if isinstance(value, Mapping):
        if (
            value.get("type") == "string"
            and value.get("contentMediaType") == "application/octet-stream"
        ):
            # `contentMediaType` is valid OpenAPI 3.1, but Swagger UI needs this
            # compatibility hint before it renders an <input type="file">.
            value.setdefault("format", "binary")

        for nested_value in value.values():
            _add_swagger_file_format(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            _add_swagger_file_format(nested_value)


_generated_openapi = app.openapi


def custom_openapi() -> dict[str, Any]:
    schema = _generated_openapi()
    _add_swagger_file_format(schema)
    return schema


app.openapi = custom_openapi
# TODO: Need to see about the logger settings and how to use it properly
logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_request(request: Request, call_next):
    request_id = request.state.request_id
    method = request.method
    url = request.url.path
    logger.info(f"[{request_id}] Incoming request: {method} {url}")
    response = await call_next(request)
    logger.info(f"[{request_id}] Response status: {response.status_code}")
    return response

# TODO: Need to check the meaning for this decorator
@app.middleware("http")
async def request_id(
    request: Request,
    call_next
):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, database_exception_handler)
# TODO: Need to check for Unhandled Exception
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/")
def root():
    return {
        "message": "App is running"
    }
