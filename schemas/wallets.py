from uuid import UUID

from pydantic import BaseModel, PositiveFloat


class BaseWalletSchema(BaseModel):
    balance: PositiveFloat = 0.0


class CreateWalletSchema(BaseWalletSchema):
    pass


class GetWalletSchema(BaseWalletSchema):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True