import asyncio

from src.repository.repository import Database
from src.utils.utils import get_logger
from src.core.config import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD


db = Database(host=DATABASE_HOST,
              port=DATABASE_PORT,
              dbname=DATABASE_NAME,
              user=DATABASE_USER,
              password=DATABASE_PASSWORD)

logger = get_logger(__name__)


# авторизация в бд если еще нет
async def insert_user_service(mail: str, google: str, given_name: str, family_name: str, picture: str) -> dict:
    result = await db.create_user(mail, google, given_name, family_name, picture)
    if result is False:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': result}


# сверка авторизованых пользователей
async def get_user_by_google_id_service(google_id: str) -> dict:
    result = await db.get_users(google_id)
    if result is False:
        return {'success': False, 'service_message': 'Данного google_id нету'}
    return {'success': True, 'service_message': result}


# создание диалога
async def init_user_dialog_service(user_id: int, dialog_name: str) -> dict:
    dialogs = await db.get_dialogs(user_id)
    if dialogs is False:
        return {'success': False, 'service_message': 'Ошибка при получении диалогов'}
    if len(dialogs) <= 4:
        dialog_id = await db.create_dialog(user_id, dialog_name)
        if dialog_id:
            return {'success': True, 'service_message': dialog_id}
        else:
            return {'success': False, 'service_message': 500}
    logger.info(f"Пользователь id:{user_id} имеет больше 5 диалогов")
    return {'success': False, 'service_message': 403}


# удаление таблицы диалога
async def delete_user_dialog_service(user_id: int, dialog_id: int) -> dict:
    result = await db.delete_dialog(user_id, dialog_id)
    if result is False:
        return {'success': False, 'service_message': 'Ошибка удаления диалога'}
    if result:
        return {'success': True, 'service_message': 'Диалог удалён'}


# запрос списков диалогов
async def get_user_dialogs_service(user_id: int) -> dict:
    result = await db.get_dialogs(user_id)
    if result is False:
        return {'success': False, 'service_message': 'Ошибка запроса списка диалогов'}
    return {'success': True, 'service_message': result}


# отправка сообщения user -> AI
async def send_message_ai_service(user_id: int, dialog_id: int, text_user: str) -> dict:
    result_ownership = await db.check_dialog_ownership(user_id, dialog_id)

    # проверка чужой ли диалог
    if result_ownership is False:
        logger.warning(f"Сообщение пользователя id:{user_id} в чужой диалог id:{dialog_id}")
        return {'success': False, 'service_message': 500}

    # проверка на спам сообщения


    # выставляем флаг для блокировки
    result_flag = await db.set_ai_response_flag(user_id, dialog_id, True)
    if result_flag is False:
        return {'success': False, 'service_message': 500}

    # добавляем сообщение user
    result_user = await db.insert_message(user_id, dialog_id, text_user)
    if result_user is False:
        return {'success': False, 'service_message': 500}

    # цикл пока не появиться сообщение от Ai
    while True:
        result_answer = await db.get_ai_response_flag(user_id, dialog_id)
        if result_answer is None:
            return {'success': False, 'service_message': 500}
        if result_answer is False:
            # читаем сообщение бд
            message_ai = await db.read_ai_message(1, dialog_id)
            if message_ai is False:
                return {'success': False, 'service_message': 500}
            return {'success': True, 'service_message': message_ai.get("content")}
        await asyncio.sleep(1)


# получения сообщения users
async def get_message_users_service() -> dict:
    result = await db.read_user_message()
    if result is False:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': result}


# запись ответа AI в бд, установка флага.
async def send_message_user_service(user_id: int, dialog_id: int, content: str) -> dict:
    # запись в бд сообщения AI
    result = await db.insert_message(1, dialog_id, content)
    if result is False:
        return {'success': False, 'service_message': 500}
    # разблокировали флаг
    result_flag = await db.set_ai_response_flag(user_id, dialog_id, False)
    if result_flag is False:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': 'Сообщение записано'}


# вернуть весь контекст беседы user и AI
async def get_context_dialog_service(user_id: int, dialog_id: int) -> dict:
    result_ownership = await db.check_dialog_ownership(user_id, dialog_id)
    if result_ownership is False:
        return {'success': False, 'service_message': 500}
    result = await db.get_dialog(user_id, dialog_id)
    if result is False:
        return {'success': False, 'service_message': 'Ошибка отправки диалога'}
    return {'success': True, 'service_message': result}


# вернуть имя и картинку пользователю
async def get_context_user_service(user_id: int) -> dict:
    result = await db.get_user(user_id)
    if result is False:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': result}


# изменение name диалога
async def update_user_name_chat_service(user_id: int, dialog_id: int, dialog_name: str):
    result = await db.update_name_chat(user_id, dialog_id, dialog_name)
    if result is False:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': result}


# получение флага
async def get_ai_response_flag_service(user_id: int, dialog_id: int) -> dict:
    result = await db.get_ai_response_flag(user_id, dialog_id)
    if result is None:
        return {'success': False, 'service_message': 500}
    return {'success': True, 'service_message': result}

