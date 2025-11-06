# generate_password_hash.py
from passlib.context import CryptContext

# Initialize bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Return the bcrypt hash of a plain password."""
    return pwd_context.hash(password)

if __name__ == "__main__":
    plain_password = input("Enter password to hash: ")
    hashed = hash_password(plain_password)
    print(f"\nHashed Password:\n{hashed}\n")
