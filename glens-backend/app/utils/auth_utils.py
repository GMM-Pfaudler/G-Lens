# app/utils/auth_utils.py
from fastapi import Header, HTTPException, status, Depends
from jose import jwt, JWTError

SECRET_KEY = "Glens"
ALGORITHM = "HS256"

async def verify_token(authorization: str = Header(...)):
    """
    Verifies JWT token from Authorization header and returns the user_id.
    Expected header: Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '"
        )

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no user_id found")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
