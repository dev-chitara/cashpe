import uuid

from sqlalchemy import Column, UUID, Float, ForeignKey
from sqlalchemy.orm import Relationship

from db_setup import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Float, default=0.0)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    transactions = Relationship("Transaction", backref="wallet")


    def __str__(self):
        return f"{self.balance}"