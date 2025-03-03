from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import router as stock_router
from app.database.database import Base, engine

# Initialize database tables


# Create FastAPI app
app = FastAPI()
Base.metadata.create_all(bind=engine)
# Include router for API routes
app.include_router(stock_router, prefix="/api")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Stock Dashboard Backend"}
