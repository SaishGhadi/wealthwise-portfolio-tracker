
from fastapi.responses import JSONResponse


def not_found(message="Not found"):
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": message}
    )


def bad_request(message="Bad request"):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": message}
    )


def unauthorized(message: str = "Unauthorized access"):
    return JSONResponse(
        status_code=401,
        content={"status": "error", "message": message}
    )


def server_error(message: str = "Something went wrong"):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": message}
    )
