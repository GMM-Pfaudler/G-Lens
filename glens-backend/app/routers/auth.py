from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

SECRET_KEY = "GMMpfaulder"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login")
def login(payload: LoginRequest):
    if payload.username == "User" and payload.password == "gmmglens":
        accss_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
        token = create_access_token(
            data={"sub":payload.username},
            expires_delta=accss_token_expires
        )
        return {"access_token":token,"token_type":"bearer"}
    raise HTTPException(status_code=401,detail="Invalid credentials")


# --------------------------
# Protected Dashboard endpoint
# --------------------------
@router.get("/dashboard")
def dashboard(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    # Example dashboard data
    return {
        "message": f"Welcome to your dashboard, {username}!",
        "data": {
            "projects": ["Project A", "Project B", "Project C"],
            "notifications": 3
        }
    }