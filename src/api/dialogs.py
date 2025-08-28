from fastapi import APIRouter, HTTPException, Depends
from src.core.security import get_current_user
from src.models.models import DialogSchema, DialogNameSchema, DialogSchemaRename
from src.services.service import (
    init_user_dialog_service, delete_user_dialog_service, get_user_dialogs_service,
    get_context_dialog_service, update_user_name_chat_service, get_ai_response_flag_service,
)


router = APIRouter(prefix="/dialogs", tags=["dialogs"])


@router.post('/create')
async def create_dialog(data: DialogNameSchema,  user_id: int = Depends(get_current_user)):
    result = await init_user_dialog_service(user_id, data.dialog_name)
    if result.get('success'):
        return {'server': 'ok', 'dialog': result.get('service_message')}
    if result.get('service_message') == 403:
        raise HTTPException(status_code=result.get('service_message'), detail='Превышен лимит диалогов')
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка создания диалога')


@router.post('/delete')
async def delete_dialog(dialog: DialogSchema, user_id: int = Depends(get_current_user)):
    result = await delete_user_dialog_service(user_id, dialog.dialog_id)
    if result.get('success'):
        return {'server': 'ok', 'status': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка удаления диалога')


@router.post('/rename')
async def delete_dialog(dialog: DialogSchemaRename, user_id: int = Depends(get_current_user)):
    result = await update_user_name_chat_service(user_id, dialog.dialog_id, dialog.dialog_name)
    if result.get('success'):
        return {'server': 'ok', 'status': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка переименования диалога')


@router.post('')
async def get_dialogs(user_id: int = Depends(get_current_user)):
    result = await get_user_dialogs_service(user_id)
    if result.get('success'):
        return {'server': 'ok', 'dialogs': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка получения диалогов')


@router.get('/{dialog_id}')
async def get_dialogs_by_id(dialog_id: int, user_id: int = Depends(get_current_user)):
    result = await get_context_dialog_service(user_id, dialog_id)
    if result.get('success'):
        return {'server': 'ok', 'dialogs': result.get('service_message')}
    raise HTTPException(status_code=result.get('service_message'), detail='Ошибка при обновление диалога')


@router.get("/flag/{dialog_id}")
async def get_flag(
    dialog_id: int,
    user_id: int = Depends(get_current_user)
):
    result = await get_ai_response_flag_service(user_id, dialog_id)
    if result.get("success"):
        return {"server": "ok", "content": result.get("service_message")}
    raise HTTPException(status_code=result.get('service_message'), detail="Ошибка обновление статуса чата")
