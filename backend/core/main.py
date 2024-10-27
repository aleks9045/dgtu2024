import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.interests.routers import router as api_interests_router
from api.leves.routers import router as api_levels_router
from api.challenges.routers import router as api_challenges_router
from api.goals.routers import router as api_goals_router
from api.statuses.routers import router as api_statues_router

from config import ORIGINS, MEDIA_FOLDER

# def swagger_monkey_patch(*args, **kwargs):
#     return get_swagger_ui_html(
#         *args, **kwargs,
#         swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
#         swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")
#
#
# applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(title="FastAPI Core", version="1.0.0")

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

app.include_router(api_interests_router)
app.include_router(api_levels_router)
app.include_router(api_challenges_router)
app.include_router(api_goals_router)
app.include_router(api_statues_router)

app.mount("/media", StaticFiles(directory=MEDIA_FOLDER, check_dir=True))

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8001, log_level="info")
