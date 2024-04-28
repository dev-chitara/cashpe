import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, ForeignKey, Float, DateTime
from sqlalchemy.orm import Relationship

from db_setup import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID, ForeignKey("users.id"))
    recipient_id = Column(UUID, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    wallet_id = Column(UUID, ForeignKey("wallets.id"))

    
    def __str__(self):
        return f"{self.amount}"