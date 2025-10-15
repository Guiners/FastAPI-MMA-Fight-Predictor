from fastapi import Depends, FastAPI, Query

from app.middleware.middlewares import log_requests
from app.routers.base_fighter_router import base_fighter_router
from app.routers.extended_fighter_router import extended_fighter_router

version = "v1"

app = FastAPI(version=version)

app.middleware("http")(log_requests)
app.include_router(base_fighter_router, prefix=f"/api/{version}")
app.include_router(extended_fighter_router, prefix=f"/api/{version}")


@app.get("/")
async def root():
    return {"message": "Welcome to MMA Fight Predictor"}
