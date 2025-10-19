from fastapi.routing import APIRouter
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import date

from app.core.security import hash_password, verify_password, generate_token
from app.db.models import User
from app.schemas.user import UserOut
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post('/register', response_model=UserOut)
def regsiter(
    first_name: str = Form(min_length=6, max_length=100),
    last_name: str = Form(min_length=6, max_length=100),
    birth_date: date = Form(...),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists.")
   
    existing_email = session.query(User).filter_by(email==email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists.")

    existing_phone = session.query(User).filter_by(phone=phone).first()
    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="phone already exists.")

    user = User(first_name=first_name, last_name=last_name, 
                birth_date=birth_date, email=email, phone=phone, 
                username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post('/login')
def login(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password.")
    
    data = {
        "sub": existing_user.username,
    }
    token = generate_token(data)
    
    return {'token': token}
