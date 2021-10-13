import traceback
from datetime import datetime, timedelta
from typing import Optional, List, Union

from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from passlib.context import CryptContext

from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db import generate_engine, User
from db.Note import Note

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Session = sessionmaker(generate_engine())


class Token(BaseModel):
    access_token: str
    token_type: str


class NoteModel(BaseModel):
    title: str
    text: str


class NoteModelDb(NoteModel):
    id: int


class TokenData(BaseModel):
    username: Optional[str] = None


class UserModel(BaseModel):
    id: int
    username: str


class UserInDB(UserModel):
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[UserInDB]:
    user = User.get_by_username(username, Session)
    if user:
        return UserInDB(id=user.id, username=user.username, password=user.password)
    return None


def create_user(username: str, password: str) -> UserInDB:
    user = User.create_user(username, get_password_hash(password), Session)
    return UserInDB(id=user[0], username=user[1], password=user[2])


def authenticate_user(username: str, password: str) -> Union[bool, UserInDB]:
    user = get_user(username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)  # type:ignore
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires  # type:ignore
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@app.post("/register", response_model=Token)
async def create_account(form_data: OAuth2PasswordRequestForm = Depends()):
    user = create_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/notes/", response_model=NoteModelDb)
async def create_note(
    title: str = Form("title"),
    text: str = Form("text"),
    current_user: UserModel = Depends(get_current_active_user),
):
    note = Note.create_note(title, text, current_user.id, Session)
    return NoteModelDb(id=note[0], title=note[1], text=note[2])


@app.get("/notes/", response_model=List[NoteModelDb])
async def get_notes(current_user: UserModel = Depends(get_current_active_user)):
    notes = Note.get_by_user_id(current_user.id, Session)
    result = []
    if notes:
        for note in notes:
            result.append(NoteModelDb(id=note[0], title=note[1], text=note[2]))
    return result


@app.put("/notes/{id}", response_model=NoteModelDb)
async def edit_note(
    id: int,
    title: str = Form("title"),
    text: str = Form("text"),
    current_user: UserModel = Depends(get_current_active_user),
):
    note = Note.edit(id, title, text, current_user.id, Session)

    return NoteModelDb(id=note[0], title=note[1], text=note[2])


@app.delete("/notes/{id}")
async def delete_note(id: int, current_user: UserModel = Depends(get_current_active_user)):
    Note.delete(id, current_user.id, Session)
