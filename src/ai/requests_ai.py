from src.utils.utils import get_logger
from src.core.config import URL_AI, API_KEY_AI
import asyncio


async def send_ai(dialog_id: int, text_message: str) -> dict:
    '''
    logger = get_logger(__name__)
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'api_key': API_KEY_AI,
            }
            json_data = {
                'dialog_id': dialog_id,
                'user_message': text_message
            }
            async with session.post(URL_AI, headers=headers, json=json_data) as response:
                text = await response.text()
                logger.info(f"AI ответил. Статус: {response.status}, тело: {text}")

                if response.status == 200:
                    return text
                else:
                    logger.warning(f"AI вернул ошибку {response.status}. Диалог {dialog_id}")
                    return None
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Ошибка соединения с AI. Диалог {dialog_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Неизвестная ошибка при отправке запроса к AI. Диалог {dialog_id}: {e}")
            return None
    '''
    return {dialog_id: 'answer_ai (AI agent is not connected yet.)'}