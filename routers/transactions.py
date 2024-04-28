from typing import List
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy import or_, and_, func
import sqlalchemy
from sqlalchemy.orm import Session

from models.transactions import Transaction
from models.users import User
from schemas.transactions import CreateTransactionSchema, GetTransactionSchema
from models.wallets import Wallet
from common.auth import Auth
from db_setup import get_db


auth = Auth()


router = APIRouter(tags=["Transaction API"])


@router.post("/transactions", status_code=status.HTTP_200_OK, response_model=GetTransactionSchema)
async def transfer_funds(transaction_data: CreateTransactionSchema, user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Get the sender's wallet
    sender_wallet_object = db.query(Wallet).filter(Wallet.user_id == user.id).first()

    if not sender_wallet_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Sender's wallet not found"}
        )

    # Get the recipient's wallet
    recipient_wallet_object = db.query(Wallet).filter(Wallet.user_id == transaction_data.recipient_id).first()

    if not recipient_wallet_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Recipient's wallet not found"}
        )

    # Check if the sender has enough balance
    if sender_wallet_object.balance < transaction_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"message": "Insufficient balance"}
        )
    
    # Update the wallet balances
    sender_wallet_object.balance -= transaction_data.amount
    recipient_wallet_object.balance += transaction_data.amount

    # Create a new transaction
    new_transaction = Transaction(
        sender_id=user.id,
        recipient_id=transaction_data.recipient_id,
        amount=transaction_data.amount,
        wallet_id=sender_wallet_object.id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/transactions", response_model=List[GetTransactionSchema])
async def get_transaction_history(
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None,
    transaction_type: str = Query(None, description="Filter by 'sent' or 'received' transactions"),
    search_query: str = Query(None, description="Search by amount or recipient/sender name"),
):
    # Get the user's transactions
    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.recipient_id == user.id)
    )

    # Filter by date range
    if start_date and end_date:
        transactions = transactions.filter(
            Transaction.timestamp >= start_date, Transaction.timestamp <= end_date
        )

    elif start_date:
        transactions = transactions.filter(Transaction.timestamp >= start_date)

    elif end_date:
        transactions = transactions.filter(Transaction.timestamp <= end_date)

    # Filter by transaction type
    if transaction_type:
        if transaction_type == "sent":
            transactions = transactions.filter(Transaction.sender_id == user.id)

        elif transaction_type == "received":
            transactions = transactions.filter(Transaction.recipient_id == user.id)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"message": "Invalid transaction type"}
            )
        
    # Search by amount or recipient/sender name
    if search_query:
        users = db.query(User).filter(
            or_(
                User.mobile.ilike(f"%{search_query}%"),
                func.cast(Transaction.amount, sqlalchemy.String).ilike(f"%{search_query}%"),
            )
        )

        user_ids = [user.id for user in users]

        transactions = transactions.filter(
            or_(
                Transaction.sender_id.in_(user_ids),
                Transaction.recipient_id.in_(user_ids),
            )
        )

    transactions = transactions.all()

    return transactions