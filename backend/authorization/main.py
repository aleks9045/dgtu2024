import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.auth.routers import router as api_auth_router
from config import ORIGINS, MEDIA_FOLDER

# def swagger_monkey_patch(*args, **kwargs):
#     return get_swagger_ui_html(
#         *args, **kwargs,
#         swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
#         swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")
#
#
# applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(title="FastAPI JWT", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=False,
    allow_methods=[
        "GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
    ],
    allow_headers=[
        "Content-Type", "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods", "X-Requested-With",
        "Authorization", "X-CSRF-Token"
    ]
)  # CORS

app.include_router(api_auth_router)

app.mount("/media", StaticFiles(directory=MEDIA_FOLDER, check_dir=True))

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info")
