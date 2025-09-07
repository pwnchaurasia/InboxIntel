import os
import sys
from dotenv import load_dotenv
from starlette.responses import HTMLResponse

load_dotenv('.env')
from sqladmin import Admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from apis.routers import api_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from admin.admin_auth import AdminAuth
from admin.all_admin import admin_views
from admin.routes import router as admin_router
from db.db_conn import engine

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


admin = Admin(
    app,
    engine,
    authentication_backend=AdminAuth(secret_key=os.getenv('SECRET_KEY')),
    title="InboxIntel Admin"
)


for view in admin_views:
    try:
        admin.add_view(view)
    except Exception as e:
        print(f"Error in {e}")

# Include routers
app.include_router(api_router)
app.include_router(admin_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("landing.html", "r") as f:
        return HTMLResponse(content=f.read())

# To include in OpenAPI
@app.get("/admin-info", tags=["admin"])
async def admin_info():
    """Admin panel information"""
    return {"admin_url": "/admin", "description": "Admin panel for managing users and jobs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000, reload=True)
