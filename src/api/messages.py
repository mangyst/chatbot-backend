from fastapi import APIRouter, HTTPException, Depends, Request
from src.core.security import get_current_user
from src.services.service import get_message_users_service, send_message_user_service, send_message_ai_service
from src.schemas.schemas import DialogSchemaAIsend, UserDialogMessage
from src.core.config import API_KEY_AI


router = APIRouter(tags=["messages"])


@router.post('/send/message/ai')
async def send_message(message: UserDialogMessage, user_id: int = Depends(get_current_user)):
    result = await send_message_ai_service(user_id, message.dialog_id, message.text_user)
    if result.get('success'):
        return {'server': 'ok', 'answer_ai': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка отправки сообщения')


@router.get("/messages")
async def get_messages(request: Request):
    key = request.headers.get("X-Messages-Key")
    if key != API_KEY_AI:
        raise HTTPException(status_code=403, detail="Forbidden")
    result = await get_message_users_service()
    if result.get('success'):
        return result
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка при обновление сообщений')


@router.post('/send/message/user')
async def send_message(request: Request, data: DialogSchemaAIsend):
    key = request.headers.get("X-Messages-Key")
    if key != API_KEY_AI:
        raise HTTPException(status_code=403, detail="Forbidden")
    result = await send_message_user_service(data.user_id, data.dialog_id, data.text_user)
    if result.get('success'):
        return {'server': 'ok', 'service_message': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка отправки сообщения')
