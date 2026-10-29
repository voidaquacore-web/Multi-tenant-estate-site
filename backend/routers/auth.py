import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from db import get_conn

load_dotenv()
JWT_SECRET =os.environ['JWT_SECRET']

router = APIRouter(prefix='/auth', tags=['auth'])
bearer = HTTPBearer()

class SignupBody(BaseModel):
    agency_name: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class LoginBody(BaseModel):
    email: EmailStr
    password: str

def make_token(user_id, agency_id, role):
    payload = {
        "user_id": str(user_id),
        "agency_id": str(agency_id),
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

@router.post('/signup')
def signup(body : SignupBody):
    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    with get_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM users WHERE  email= %s", (body.email,)
        ).fetchone()

        if exists:
            raise HTTPException(400, 'This email already exists')
        agency_id = conn.execute(
            "INSERT INTO agencies (name) values (%s) RETURNING id", (body.agency_name,)
        ).fetchone()[0]
        user_id = conn.execute(
            "INSERT INTO users (agency_id, name, email, password_hash, role)"
            "VALUES (%s, %s, %s, %s, 'owner') RETURNING id", 
            (agency_id, body.name, body.email, hashed),
        ).fetchone()[0]
        return {'token': make_token(user_id, agency_id, 'owner')}

@router.post('/login')
def login(body: LoginBody):
    with get_conn() as conn:
        row = conn.execute(
            'SELECT id, agency_id, password_hash, role FROM users WHERE email = %s', (body.email,)
        ).fetchone()
        if not row or not bcrypt.checkpw(body.password.encode(), row[2].encode()):
            raise HTTPException(401, "Invaild email or password")
        return {'token': make_token(row[0], row[1], row[3])}

def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        data = jwt.decode(creds.credentials, JWT_SECRET, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        raise HTTPException(401, 'Invalid or expired token')
    return data

@router.get("/me")
def me(user=Depends(current_user)):
    return user
