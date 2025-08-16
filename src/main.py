from fastapi import FastAPI, HTTPException, Depends, Response, Request
import uvicorn
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.services.service import (get_user_by_google_id_service, insert_user_service, init_user_dialog_service,
                                  delete_user_dialog_service, get_user_dialogs_service,
                                  send_message_ai_service, get_context_dialog_service, get_context_user_service,
                                  update_user_name_chat_service, get_ai_response_flag_service)
from src.models.models import DialogSchema, DialogNameSchema, UserDialogMessage, DialogSchemaRename
from src.core.security import get_current_user, create_access_token
from src.utils.utils import get_logger
from src.core.config import ADDRESS_FRONT, GOOGLE_CLIENT_ID, HEALTH_SECRET_KEY

app = FastAPI()
logger = get_logger(__name__)


origins = [ADDRESS_FRONT,]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/create/users')
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
                raise HTTPException(status_code=500, detail="Ошибка создания пользователя")
            user_id = create_result.get('service_message')
        else:
            user_id = user_check.get('service_message')
        session_token = create_access_token({"sub": str(user_id)})
        response.set_cookie(
            key="access_token",
            value=session_token,
            httponly=True,
            max_age=60 * 60 * 24,
            secure=True,
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


@app.get('/me')
async def get_me(user_id: int = Depends(get_current_user)):
    result = await get_context_user_service(user_id)
    if result.get('success'):
        return {'server': 'ok', 'content': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка аутификации')


@app.get("/flag/{dialog_id}")
async def get_flag(
    dialog_id: int,
    user_id: int = Depends(get_current_user)
):
    result = await get_ai_response_flag_service(user_id, dialog_id)
    if result.get("success"):
        return {"server": "ok", "content": result.get("service_message")}
    raise HTTPException(status_code=500, detail="Ошибка обновление чата")


@app.post('/dialogs/create')
async def create_dialog(data: DialogNameSchema,  user_id: int = Depends(get_current_user)):
    result = await init_user_dialog_service(user_id, data.dialog_name)
    if result.get('success'):
        return {'server': 'ok', 'dialog': result.get('service_message')}
    if result.get('service_message') == 403:
        raise HTTPException(status_code=403, detail='Превышен лимит диалогов')
    raise HTTPException(status_code=500, detail='Ошибка создания диалога')


@app.post('/dialogs/delete')
async def delete_dialog(dialog: DialogSchema, user_id: int = Depends(get_current_user)):
    result = await delete_user_dialog_service(user_id, dialog.dialog_id)
    if result.get('success'):
        return {'server': 'ok', 'status': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка удаления диалога')


@app.post('/dialogs/rename')
async def delete_dialog(dialog: DialogSchemaRename, user_id: int = Depends(get_current_user)):
    result = await update_user_name_chat_service(user_id, dialog.dialog_id, dialog.dialog_name)
    if result.get('success'):
        return {'server': 'ok', 'status': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка переименования диалога')


@app.post('/dialogs')
async def get_dialogs(user_id: int = Depends(get_current_user)):
    result = await get_user_dialogs_service(user_id)
    if result.get('success'):
        return {'server': 'ok', 'dialogs': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка получения диалогов')


@app.post('/send/message/ai')
async def send_message(message: UserDialogMessage, user_id: int = Depends(get_current_user)):
    result = await send_message_ai_service(user_id, message.dialog_id, message.text_user)
    if result.get('success'):
        return {'server': 'ok', 'answer_ai': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка отправки сообщения')


@app.get('/dialogs/{dialog_id}')
async def get_dialogs(dialog_id: int, user_id: int = Depends(get_current_user)):
    result = await get_context_dialog_service(user_id, dialog_id)
    if result.get('success'):
        return {'server': 'ok', 'dialogs': result.get('service_message')}
    raise HTTPException(status_code=500, detail='Ошибка при обновление диалога')


@app.get("/health")
async def health(request: Request):
    key = request.headers.get("X-Health-Key")
    if key != HEALTH_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
