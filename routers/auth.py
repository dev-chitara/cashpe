from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from common.utils import hash_pass, verify_password
from common.auth import Auth, parse_json_body
from models.users import User
from schemas.users import CreateUserSchema, GetUserSchema
from schemas.auth import CustomOAuth2PasswordRequestForm
from db_setup import get_db


router = APIRouter(
    tags=["Authentication"]
)

auth = Auth()


@router.post("/signup", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def registration(signup_data: CreateUserSchema, db: Session=Depends(get_db)):
    user_data = signup_data.model_dump()
    
    user = db.query(User).filter(User.mobile == user_data.get("mobile")).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "User already exists!"}
        )

    password = user_data.pop("password")

    user_object = User(password=hash_pass(password), **user_data)
    
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    
    return user_object


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data: CustomOAuth2PasswordRequestForm = Depends(parse_json_body), db: Session = Depends(get_db)):
    user_object = db.query(User).filter(User.mobile == login_data.mobile).first()

    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"message": "user does not exist!"}
        )
    
    if not verify_password(login_data.password, user_object.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"message": "password does not match"}
        )
    
    access_token = auth.create_access_token(subject=user_object.id)

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }