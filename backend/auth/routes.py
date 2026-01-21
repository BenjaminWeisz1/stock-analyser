from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db.database import get_connection
from backend.utils.crypto import generate_salt, hash_password, verify_password
from backend.auth.security import authenticated_users

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: AuthRequest):
    email = data.email
    password = data.password
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    )

    row = cursor.fetchone()

    if row:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    salt = generate_salt()
    password_hash = hash_password(password, salt)

    cursor.execute(
        "INSERT INTO users (email, salt, password_hash) VALUES (?, ?, ?)",
        (email, salt, password_hash)
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: AuthRequest):
    email = data.email
    password = data.password

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT salt, password_hash FROM users WHERE email = ?",
        (email,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Email not registered")
    
    if not verify_password(password, row["salt"], row["password_hash"]):
        raise HTTPException(status_code=401, detail="Password does not match")
    
    authenticated_users.add(email)

    return {"message": "Login successful"}
