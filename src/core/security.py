from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request

from src.utils.utils import get_logger
from src.core.config import SECRET_KEY_JWT, ALGORITHM

logger = get_logger(__name__)


# создает jwt-токен
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=1))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)


# декодирует и проверяет jwt-токен
def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("JWT ошибка: отсутствует 'sub'")
            raise HTTPException(status_code=401, detail="Недействительный токен")
        return int(user_id)
    except JWTError as e:
        logger.error(f"JWT ошибка: {e}")
        raise HTTPException(status_code=401, detail="Недействительный или просроченный токен")


# извлекает текущего пользователя
async def get_current_user(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Необходима авторизация")
    return decode_token(token)




