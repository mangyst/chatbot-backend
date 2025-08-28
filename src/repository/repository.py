from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.utils.utils import get_logger


class Database:
    def __init__(self, host, port, dbname, user, password):
        self.engine = create_async_engine(
            f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}',
            echo=False
        )
        self.async_session = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.logger = get_logger(__name__)

    # Сверка пользователя в БД
    async def get_users(self, google_id: str) -> int | bool:
        query = text("""
            SELECT user_id FROM users
            WHERE google_id = :google_id;
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'google_id': google_id})
                user_id = result.scalar()
                if user_id is not None:
                    return user_id
                else:
                    self.logger.info(f"Пользователь с google_id='{google_id}' не найден.")
                    return False
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка при получении пользователя: {e}")
                return False

    # внесения пользователя в бд
    async def create_user(self, mail: str, google_id: str, given_name: str, family_name: str,
                          picture: str) -> int | bool:
        query = text("""
            INSERT INTO users(mail, google_id, given_name, family_name, picture)
            VALUES(:mail, :google_id, :given_name, :family_name, :picture)
            RETURNING user_id;
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {
                    "mail": mail,
                    "google_id": google_id,
                    "given_name": given_name,
                    "family_name": family_name,
                    "picture": picture,
                })
                await session.commit()
                user_id = result.scalar()
                self.logger.info(f"Пользователь с почтой '{mail}' успешно создан с user_id={user_id}")
                return user_id
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Ошибка при создании пользователя с почтой '{mail}': {e}")
                return False

    # проверка принадлежности диалога
    async def check_dialog_ownership(self, user_id: int, dialog_id: int) -> bool:
        query = text("""
            SELECT dialog_id FROM dialogs
            WHERE user_id = :user_id AND dialog_id = :dialog_id
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {"user_id": user_id, "dialog_id": dialog_id})
                dialog = result.scalar_one_or_none()
                if dialog is None:
                    self.logger.warning(f"Доступ запрещён пользователь id:{user_id} не владеет диалогом id:{dialog_id}")
                    return False
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Ошибка при проверке доступа к диалогу id:{dialog_id} пользователя id:{user_id}: {e}")
                return False

    # внести user_id в dialogs (КНОПКА создать диалог)
    async def create_dialog(self, user_id: int, dialog_name: str) -> int | bool:
        query = text("""
            INSERT INTO dialogs(user_id, dialog_name)
            VALUES(:user_id, :dialog_name)
            RETURNING dialog_id;
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'user_id': user_id, 'dialog_name': dialog_name})
                await session.commit()
                dialog_id = result.scalar()
                self.logger.info(f"Пользователь id:{user_id} успешно создал диалог id:{dialog_id}")
                return dialog_id
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Ошибка при создании диалога. Пользователь id:{user_id}: {e}")
                return False

    # удаление dialog_id из dialogs
    async def delete_dialog(self, user_id: int, dialog_id: int) -> bool:
        query = text("""
            DELETE FROM dialogs
            WHERE user_id = :user_id AND dialog_id = :dialog_id;
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'user_id': user_id, 'dialog_id': dialog_id})
                await session.commit()
                if result.rowcount == 0:
                    self.logger.warning(f"Диалог id:{dialog_id} не найден или не принадлежит пользователю id:{user_id}")
                    return False
                self.logger.info(f"Пользователь id:{user_id} удалил диалог id:{dialog_id}")
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Ошибка при удаление диалога. Пользователь id:{user_id}- {e}")
                return False

    # запрос на список dialogs пользователя
    async def get_dialogs(self, user_id: int) -> list | bool:
        query = text("""
            SELECT dialog_id, dialog_name 
            FROM dialogs
            WHERE user_id = :user_id
            ORDER BY dialog_id;
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'user_id': user_id})
                rows = result.mappings().all()
                dialogs = [dict(row) for row in rows]
                self.logger.info(f"Получено {len(dialogs)} диалог(ов) пользователя id:{user_id}")
                return dialogs
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка при получении диалогов пользователя id:{user_id}: {e}")
                return False

    # отправка сообщения в messages
    async def insert_message(self, user_id: int, dialog_id: int, content: str) -> bool:
        query = text("""
            INSERT INTO messages(dialog_id, user_id, content)
            VALUES(:dialog_id, :user_id, :content)
        """)
        async with self.async_session() as session:
            try:
                await session.execute(query, {
                    'dialog_id': dialog_id,
                    'user_id': user_id,
                    'content': content
                })
                await session.commit()
                self.logger.info(f"Пользователь id:{user_id} записал сообщение в диалог id:{dialog_id}")
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Ошибка при записи сообщения пользователя id:{user_id}: {e}")
                return False

    # получить контекст диалога
    async def get_dialog(self, user_id: int, dialog_id: int) -> bool | list:
        query = text("""
            SELECT user_id, content FROM messages
            WHERE dialog_id = :dialog_id
            ORDER BY created_at
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'dialog_id': dialog_id})
                rows = result.mappings().all()
                dialog = [
                    {
                        "role": "bot" if row["user_id"] == 1 else "user",
                        "content": row["content"]
                    }
                    for row in rows
                ]
                self.logger.info(f"Пользователь:{user_id} получил диалог id:{dialog_id}")
                return dialog
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка получения диалога id:{dialog_id} пользователям id: {user_id}: {e}")
                return False

    # получить имя, фамилию, аватарка
    async def get_user(self, user_id: int) -> bool | list:
        query = text("""
                    SELECT given_name,
                    family_name,
                    picture FROM users
                    WHERE user_id = :user_id
                """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {'user_id': user_id})
                rows = result.mappings().all()
                content_user = [dict(row) for row in rows]
                self.logger.info(f"Пользователь:{user_id} получил дату для /me")
                return content_user
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка получения даты для /me пользователем id: {user_id}: {e}")
                return False

    # Переименовать диалог
    async def update_name_chat(self, user_id: int, dialog_id: int, dialog_name: str) -> bool:
        query = text("""
            UPDATE dialogs
            SET dialog_name = :dialog_name
            WHERE user_id = :user_id AND dialog_id = :dialog_id
            RETURNING dialog_id
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {
                    'dialog_name': dialog_name,
                    'dialog_id': dialog_id,
                    'user_id': user_id
                })
                await session.commit()
                updated = result.scalar_one_or_none()
                if updated is None:
                    self.logger.error(f"Не найден диалог {dialog_id} для переименования пользователем {user_id}")
                    return False

                self.logger.info(f"Пользователь id:{user_id} переименовал диалог id:{dialog_id} в '{dialog_name}'")
                return True
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка переименования диалога пользователем id: {user_id}: {e}")
                return False

    # установка флага чата
    async def set_ai_response_flag(self, user_id: int, dialog_id: int, flag_status: bool) -> bool:
        query = text("""
            UPDATE dialogs
            SET status_flag = :flag_status
            WHERE user_id = :user_id AND dialog_id = :dialog_id
            RETURNING dialog_id
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {
                    'user_id': user_id,
                    'dialog_id': dialog_id,
                    'flag_status': flag_status
                })
                await session.commit()
                updated = result.scalar_one_or_none()
                if updated is None:
                    self.logger.error(f"Не найден диалог {dialog_id} для пользователя {user_id}")
                    return False
                self.logger.info(f"Диалог id:{dialog_id} — статус флага: {flag_status}")
                return True
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка установки флага для пользователя {user_id}: {e}")
                return False

    # получение флага
    async def get_ai_response_flag(self, user_id: int, dialog_id: int) -> bool | None:
        query = text("""
            SELECT status_flag
            FROM dialogs
            WHERE user_id = :user_id AND dialog_id = :dialog_id
        """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {
                    'user_id': user_id,
                    'dialog_id': dialog_id
                })
                flag = result.scalar_one_or_none()
                if flag is None:
                    self.logger.warning(f"Флаг не найден для диалога {dialog_id} пользователя {user_id}")
                    return None
                self.logger.info(f"Пользователь {user_id} получил флаг: {flag}")
                return flag
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка получения флага для чата {dialog_id} пользователя {user_id}: {e}")
                return None

    async def read_ai_message(self, user_id: int, dialog_id: int) -> bool | dict:
        query = text("""
            SELECT content FROM messages
            WHERE dialog_id = :dialog_id AND user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 1
           """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query, {
                    'user_id': user_id,
                    'dialog_id': dialog_id
                })
                content = result.scalar_one_or_none()
                if content is None:
                    self.logger.warning(f"Последние сообщение: {user_id} в диалоге: {dialog_id} не найдено")
                    return False
                self.logger.info(f"Пользователь {user_id} получил последнее сообщение")
                return {'content': content}
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка получения последнего сообщения для чата {dialog_id} пользователя {user_id}: {e}")
                return False

    async def read_user_message(self) -> bool | list:
        query = text("""
            SELECT messages.user_id, messages.dialog_id, messages.content FROM messages
            JOIN dialogs ON messages.dialog_id = dialogs.dialog_id
            WHERE dialogs.status_flag = true AND messages.user_id <> 1
              """)
        async with self.async_session() as session:
            try:
                result = await session.execute(query)
                rows = result.mappings().all()
                content_messages = [dict(row) for row in rows]
                self.logger.info(f"AI:получил диалоги")
                return content_messages
            except SQLAlchemyError as e:
                self.logger.error(f"Ошибка AI не получила диалоги")
                return False
