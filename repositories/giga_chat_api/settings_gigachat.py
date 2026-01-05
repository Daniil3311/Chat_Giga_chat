import os

from gigachat import GigaChat

giga = GigaChat(
        credentials=os.getenv("GIGACHAT_API_KEY"),
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False  # для локальной разработки
                )
