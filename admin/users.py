from fastapi import FastAPI
from sqladmin import Admin, ModelView
from db.models import User



class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]


