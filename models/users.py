import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import Relationship

from db_setup import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mobile = Column(String(15), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    wallet = Relationship("Wallet", backref="user", uselist=False)

    sent_transactions = Relationship("Transaction", foreign_keys="[Transaction.sender_id]", backref="sender")
    received_transactions = Relationship("Transaction", foreign_keys="[Transaction.recipient_id]", backref="recipient")


    def __str__(self):
        return f"{self.name}"