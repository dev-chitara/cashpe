from uuid import UUID

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    mobile: str
    password: str


class GetUserSchema(BaseModel):
    id: UUID
    mobile: str

    class Config:
        from_attributes = True