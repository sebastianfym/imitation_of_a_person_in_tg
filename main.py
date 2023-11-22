import asyncio
import datetime
from pyrogram import filters
from pyrogram.types import Message
from sqlalchemy import select, insert
from db import init_db, async_session as session
from models import User
from config import client, logger
from services import send_photo


@client.on_message(filters.command("users_today", prefixes='/') & filters.private)
async def users_today(client_object, message: Message):
    try:
        query = select(User).where(User.created_date == datetime.datetime.now().date())
        async with session() as s:
            res = await s.execute(query)
            res = res.fetchall()
            text = f'Количество пользователей зарегестрированых сегодня: {len(res)}'
    except Exception as e:
        text = e

    await client_object.send_message(message.chat.id, text)
    logger.info(f"Сообщение: {text} в чате: {message.chat.id}, отправлено в: {datetime.datetime.now()}")


async def funnel(user_id, trigger):
    chat_id = user_id

    await asyncio.sleep(600)
    await client.send_message(chat_id, "Добрый день!")
    logger.info(f"Сообщение: {'Добрый день!'} в чате: {user_id}, отправлено в: {datetime.datetime.now()}")

    await asyncio.sleep(5400)
    await client.send_message(chat_id, "Подготовил для Вас материал")
    logger.info(f"Сообщение: {'Подготовил для Вас материал'} в чате: {user_id}, отправлено в: {datetime.datetime.now()}")
    await send_photo(client, chat_id)
    logger.info(f"Сообщение с изображением в чате: {user_id}, отправлено в: {datetime.datetime.now()}")

    await asyncio.sleep(7200)

    history_chat_list = [message.text async for message in client.get_chat_history(chat_id, limit=3)]

    if trigger not in history_chat_list:
        await client.send_message(chat_id, "Скоро вернусь с новым материалом!")
        logger.info(f"Сообщение: {'Скоро вернусь с новым материалом!'} в чате: {user_id}, отправлено в: {datetime.datetime.now()}")


@client.on_message(filters.private)
async def start_funnel(client_object, message: Message):
    chat_id = int(message.from_user.id)
    user = select(User).where(User.tg_id == chat_id)
    res = await session().execute(user)
    user = res.fetchone()

    if user is None:
        query = insert(User).values(
            tg_id=int(message.from_user.id),
            username=message.from_user.username,
            created_date=datetime.datetime.now()
        )
        try:
            async with session() as s:
                await s.execute(query)
                await s.commit()
        except Exception as e:
            return f'Произошла ошибка: {e}'

    if message.text == "Хорошего дня":
        return

    asyncio.create_task(funnel(chat_id, trigger="Хорошего дня"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    client.run()
