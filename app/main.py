from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware  # Import the CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes, invite_routes
from app.utils.api_description import getDescription
from app.minio_setup import create_minio_bucket

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
# CORS middleware configuration
# This middleware will enable CORS and allow requests from any origin
# It can be configured to allow specific methods, headers, and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed to access the server, ["*"] allows all
    allow_credentials=True,  # Support credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed HTTP headers
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)
    create_minio_bucket()

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

@app.get("/accepted",include_in_schema=False, response_class=HTMLResponse)
async def verified_page():
    # Return an HTML response with the message
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verification</title>
    </head>
    <body>
        <h1 style="text-align: center; color: green;">Invitation successfully accepted!</h1>
    </body>
    </html>
    """
    return html_content

app.include_router(user_routes.router)
app.include_router(invite_routes.router)