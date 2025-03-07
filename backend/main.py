from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import router as stock_router
from app.database.database import Base, engine
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Add in main.py
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(middleware=[
    Middleware(TrustedHostMiddleware, allowed_hosts=["localhost"]),
])
Base.metadata.create_all(bind=engine)
# Include router for API routes
app.include_router(stock_router, prefix="/api")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Stock Dashboard Backend"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )