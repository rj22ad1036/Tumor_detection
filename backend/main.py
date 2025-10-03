import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth,hospitals
from models import Base
from database import engine
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

# Allowed origins
origins = [
    "http://localhost:5173"
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # restrict to frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(hospitals.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
