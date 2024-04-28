from uuid import UUID

from pydantic import BaseModel, PositiveFloat


class BaseTransactionSchema(BaseModel):
    amount: PositiveFloat


class CreateTransactionSchema(BaseTransactionSchema):
    recipient_id: UUID


class GetTransactionSchema(BaseTransactionSchema):
    id: UUID
    sender_id: UUID
    recipient_id: UUID
    wallet_id: UUID

    class Config:
        from_attributes = True 