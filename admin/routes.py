import os

from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.db_conn import get_db
from admin.admin_auth import AdminAuth

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")
auth_backend = AdminAuth(secret_key=os.getenv('SECRET_KEY'))

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("admin/admin_login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if await auth_backend.login(username, password):
        response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
        # Set session/cookie here for authentication
        response.set_cookie(key="admin_session", value="authenticated")
        return response
    else:
        return templates.TemplateResponse(
            "admin/admin_login.html",
            {"request": request, "error": "Invalid credentials"}
        )

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="admin_session")
    return response
