from uuid import UUID

from pydantic import BaseModel, PositiveFloat


class BaseTransactionSchema(BaseModel):
    amount: PositiveFloat
    transaction_type: str


class DepositeTransactionSchema(BaseTransactionSchema):
    pass


class CreateTransactionSchema(BaseTransactionSchema):
    recipient_id: UUID


class GetTransactionSchema(BaseTransactionSchema):
    id: UUID
    sender_id: UUID | None=None
    recipient_id: UUID | None=None
    wallet_id: UUID

    class Config:
        from_attributes = True 