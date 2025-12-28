from typing import List

from gigachat import GigaChat
import os
import logging

# logger = logging.getLogger(__name__)
#
# # БЕЗОПАСНОСТЬ: читаем API ключ из переменной окружения
# api_key = os.getenv("GIGACHAT_API_KEY")
#
giga = GigaChat(
        credentials='ZGRjNjc4ZmItZjQzNC00MzE5LWE2MzEtNGM3N2RlZTEyYWY1OmQyODA2Njc2LWVhMzAtNDcyYi1hNTQzLWZjOWZiMmY0ODYwMQ==',
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False  # для локальной разработки
    )


def get_giga_client():
    """Получить клиент GigaChat, инициализируя его при первом использовании"""
    global giga
    if giga is None:
        api_key = os.getenv("GIGACHAT_API_KEY")
        if not api_key:
            raise ValueError(
                "GIGACHAT_API_KEY environment variable is not set. Please set it in .env file or environment variables.")

        # Инициализация GigaChat клиента
        # Примечание: таймауты настраиваются внутри библиотеки, при необходимости
        # можно настроить через переменные окружения или параметры библиотеки
        giga = GigaChat(
            credentials=api_key,
            scope="GIGACHAT_API_PERS",  # Обязательный параметр для аутентификации
            verify_ssl_certs=False  # для локальной разработки
        )
    return giga


def get_embedding(text: str) -> List[float]:
    client = get_giga_client()
    response = client.embed({"input": text})
    return response.data[0].embedding