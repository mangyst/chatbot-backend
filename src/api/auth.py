from fastapi import APIRouter, HTTPException, Depends, Response, Request
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from fastapi.responses import JSONResponse

from src.core.config import GOOGLE_CLIENT_ID, SECURE_HTTP_HTTPS
from src.core.security import get_current_user, create_access_token
from src.services.service import (
    get_user_by_google_id_service, insert_user_service, get_context_user_service
)
from src.utils.utils import get_logger


router = APIRouter(tags=["auth"])
logger = get_logger(__name__)


@router.post('/create/users')
async def create_users(request: Request, response: Response):
    data = await request.json()
    token = data.get('token')
    if not token:
        raise HTTPException(status_code=400, detail="Gmail токен потерян")
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        user_google_id = idinfo['sub']
        user_email = idinfo.get('email')
        user_given_name = idinfo.get('given_name')
        user_family_name = idinfo.get('family_name')
        user_picture = idinfo.get('picture')
        user_check = await get_user_by_google_id_service(user_google_id)
        if not user_check.get('success'):
            create_result = await insert_user_service(user_email, user_google_id, user_given_name, user_family_name,
                                              user_picture)
            if not create_result.get('success'):
                raise HTTPException(status_code=create_result.get('service_message'), detail="Ошибка создания пользователя")
            user_id = create_result.get('service_message')
        else:
            user_id = user_check.get('service_message')
        session_token = create_access_token({"sub": str(user_id)})
        response.set_cookie(
            key="access_token",
            value=session_token,
            httponly=True,
            max_age=60 * 60 * 24,
            secure=SECURE_HTTP_HTTPS,
            samesite="Lax"
        )
        return {
            "status": "successful",
            "email": user_email,
            "given_name": user_given_name,
            "family_name": user_family_name,
            "picture": user_picture
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Неверный токен Google")
    except Exception as e:
        logger.error(f"Ошибка создания/аутификации пользователя: {e}")
        return JSONResponse(status_code=500, content='Ошибка создания/аутификации')


@router.get('/me')
async def get_me(user_id: int = Depends(get_current_user)):
    result = await get_context_user_service(user_id)
    if result.get('success'):
        return {'server': 'ok', 'content': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка аутификации')


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )

    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=SECURE_HTTP_HTTPS,
        samesite="Lax",
        path="/",
        max_age=0,
        expires=0
    )

    return {"server": "ok"}
