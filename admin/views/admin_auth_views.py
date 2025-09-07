import os

from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.db_conn import get_db
from db.models import User
from admin.admin_auth import AdminAuth
from utils.validators import Validators
from services.user_service import UserService

templates = Jinja2Templates(directory="templates")


class AdminAuthView:
    def __init__(self):
        self.router = APIRouter(prefix="/admin", tags=["admin"])
        self.auth_backend = AdminAuth(secret_key=os.getenv('SECRET_KEY'))
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route("/login", self.login_get, methods=["GET"], response_class=HTMLResponse)
        self.router.add_api_route("/login", self.login_post, methods=["POST"])
        self.router.add_api_route("/register", self.register_get, methods=["GET"], response_class=HTMLResponse)
        self.router.add_api_route("/register", self.register_post, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["GET"])

    async def login_get(self, request: Request):
        return templates.TemplateResponse("admin/admin_login.html", {"request": request})

    async def login_post(self, request: Request):
        db = next(get_db())
        form = await request.form()
        phone_number = form['phone_number']
        password = form['password']
        user_exists = UserService.get_user_by_phone(phone_number=phone_number, db=db)

        if not user_exists:
            return templates.TemplateResponse(
                "admin/admin_login.html",
                {"request": request, "error": "User not found, Please check creds or register."}
            )

        return True

    async def logout(self, request: Request):
        pass



    async def register_get(self, request: Request):
        return templates.TemplateResponse("admin/admin_register.html", {"request": request})

    async def register_post(self, request: Request, name: str = Form(...), phone_number: str = Form(...),
                            password: str = Form(...), db: Session = Depends(get_db)):
        # Registration logic here
        try:
            db = next(get_db())
            form = await request.form()
            phone_number = form['phone_number']
            password = form['password']
            name = form['name']
            # Validate inputs
            if not phone_number or not password or not name:
                return templates.TemplateResponse(
                    "admin/admin_register.html",
                    {"request": request, "error": "All fields are required"}
                )

            is_valid = Validators.validate_password(password=password)
            if not is_valid:
                return templates.TemplateResponse(
                    "admin/admin_register.html",
                    {"request": request, "error": "Not a valid password"}
                )

            user_exists = UserService.get_user_by_phone(phone_number=phone_number, db=db)
            if user_exists:
                return templates.TemplateResponse(
                    "admin_register.html",
                    {"request": request, "error": "User with this phone number already exists"}
                )

            user = UserService.create_user(name=name, phone_number=phone_number, password=password, db=db)
            if user:
                return RedirectResponse(
                    url="/admin/login?message=Registration successful",
                    status_code=status.HTTP_302_FOUND
                )

            return templates.TemplateResponse(
                "admin_register.html",
                {"request": request, "error": "Registration failed. Please try again."}
            )
        except Exception as e:
            return templates.TemplateResponse(
                "admin/admin_register.html",
                {"request": request, "error": "Registration failed. Please try again."}
            )



async def logout(self):
        response = RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key="admin_session")
        return response


# Create instance
admin_auth_view_ins = AdminAuthView()