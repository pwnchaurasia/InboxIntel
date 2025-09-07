from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union
from datetime import datetime
from enum import Enum


# Auth related schemas
class UserRegistration(BaseModel):
    phone_number: str

class OTPVerification(BaseModel):
    phone_number: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str