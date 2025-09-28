from pydantic import BaseModel, EmailStr


class AdminModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminModelResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True