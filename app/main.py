from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import auth, users, horses, market, rental

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(horses.router, prefix=f"{settings.API_V1_STR}/horses", tags=["horses"])
app.include_router(market.router, prefix=f"{settings.API_V1_STR}/market", tags=["market"])
app.include_router(rental.router, prefix=f"{settings.API_V1_STR}/rental", tags=["rental"])

@app.get("/")
def root():
    return {
        "message": "Welcome to Horse Board API",
        "version": settings.VERSION,
        "docs_url": f"/docs",
        "redoc_url": f"/redoc",
    } 