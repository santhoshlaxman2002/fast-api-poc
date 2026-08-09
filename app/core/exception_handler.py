from fastapi import Request
from fastapi.responses import JSONResponse

async def app_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error":{
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )

async def database_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": {
                "code": "DATABASE_CONSTRAINT_ERROR",
                "message": "Database constraint violation"
            }
        }
    )