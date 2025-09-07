from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqladmin.authentication import AuthenticationBackend
from db.models import User
from db.db_conn import engine, get_db
from sqlalchemy.orm import Session
import secrets

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        db = next(get_db())
        form = await request.form()
        username = form['username']
        password = form['password']
        user = db.query(User).filter(
            User.phone_number == username,
            User.is_admin == True
        ).first()
        if user and user.password_hash:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            return pwd_context.verify(password, user.password_hash)
        return False

    async def logout(self):
        pass

    async def authenticate(self):
        pass
