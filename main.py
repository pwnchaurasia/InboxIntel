import os
import sys
from dotenv import load_dotenv
from starlette.responses import HTMLResponse

load_dotenv('.env')
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from apis.routers import api_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="InboxIntel API",
    description="Secure local file sharing and content management system with polymorphic content support",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(api_router)




@app.get("/", response_class=HTMLResponse)
async def root():
    with open("landing.html", "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000, reload=True)
