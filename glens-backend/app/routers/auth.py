from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.core.database import get_session
from app.models.login import Login 

router = APIRouter()

# ----------------------------------
# JWT Configuration
# ----------------------------------
SECRET_KEY = "GMMpfaulder"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------
# Schemas
# ----------------------------------
class LoginRequest(BaseModel):
    user_id: str
    password: str


# ----------------------------------
# Helper Functions
# ----------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ----------------------------------
# Login Endpoint (DB-based)
# ----------------------------------
@router.post("/login")
async def login(payload: LoginRequest, db=Depends(get_session)):
    # 1️⃣ Find user by email/user_id
    query = select(Login).where(Login.user_id == payload.user_id)
    result = await db.execute(query)
    user = result.scalars().first()

    # 2️⃣ Validate user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3️⃣ Verify hashed password
    if not pwd_context.verify(payload.password.strip(), user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 4️⃣ Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    token = create_access_token(
        data={"sub": user.user_id, "role": user.role.value},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.value,
        "user_id": user.user_id,
    }


# ----------------------------------
# Protected Dashboard endpoint
# ----------------------------------
@router.get("/dashboard")
def dashboard(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    return {
        "message": f"Welcome to your dashboard, {user_id}!",
        "data": {
            "projects": ["Project A", "Project B", "Project C"],
            "notifications": 3,
        },
    }


# ----------------------------------
# Helper: get current user from token
# ----------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extracts the current user_id and role from JWT.
    Raises 401 if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")