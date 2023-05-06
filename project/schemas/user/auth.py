from pydantic import BaseModel, EmailStr


class AuthForm(BaseModel):
    email: EmailStr
    password: str
