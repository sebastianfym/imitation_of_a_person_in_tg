async def send_photo(client, chat_id):
    chat_id = chat_id
    photo_path = "img/img.jpg"
    # Тут я поставил статичное фото из папки, т.к. в тз было указано "любое фото", но в зависимости от требований это все легко изменяется

    await client.send_photo(
        chat_id=chat_id,
        photo=photo_path,
        caption=""  # Описание по желанию
    )

