import uuid
import logging
from fastapi import FastAPI, Request
from app.routers import users,products,auth
from app.core.exceptions import AppException
from app.core.exception_handler import app_exception_handler, validation_exception_handler, generic_exception_handler, database_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

app = FastAPI()
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
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/")
def root():
    return {
        "message": "App is running"
    }
