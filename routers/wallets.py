from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from models.wallets import Wallet
from models.users import User
from schemas.wallets import CreateWalletSchema, GetWalletSchema
from common.auth import Auth
from db_setup import get_db


auth = Auth()


router = APIRouter(tags=["Wallet API"])


@router.post("/wallets", status_code=status.HTTP_200_OK, response_model=GetWalletSchema)
async def add_funds(wallet_data: CreateWalletSchema, user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Check if the user has an existing wallet
    existing_wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()

    if existing_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"message": "Wallet already exists for the user"}
        )

    # Create a new wallet
    wallet_object = Wallet(user_id=user.id, balance=wallet_data.balance)
    db.add(wallet_object)
    db.commit()
    db.refresh(wallet_object)

    return wallet_object


@router.get("/wallets/balance", status_code=status.HTTP_200_OK, response_model=GetWalletSchema)
async def get_wallet_balance(user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Get the user's wallet
    wallet_object = db.query(Wallet).filter(Wallet.user_id == user.id).first()

    if not wallet_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Wallet not found for the user"}
        )

    return wallet_object