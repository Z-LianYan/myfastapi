from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=2)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm="HS256"
    )


def verify_access_token(token: str):
    return jwt.decode(
        token,
       settings.JWT_SECRET,
       algorithms=["HS256"]
   )