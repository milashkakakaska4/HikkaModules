import requests
from .. import loader, utils  # Телеграм модульный фреймворк
import logging
import asyncio

logger = logging.getLogger(__name__)

@loader.tds
class WWTModule(loader.Module):
    """Модуль для генерации ответов от ChatGPT через onlysq API. Разработчик: @xqss_DEVELOPER"""

    strings = {"name": "WWTModule"}

    async def client_ready(self, client, db):
        self.client = client

    async def wwtcmd(self, message):
        """
        .wwt {предмет} - Генерация ответа от ChatGPT по вопросу: что победит {предмет} через onlysq API.
        """
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "⚠️ <b>Пожалуйста, укажите предмет для запроса.</b>")
            return

        subject = args.strip()

        # Отправка сообщения о генерации
        generation_message = await utils.answer(message, "⏳ <b>Генерация ответа...</b>")

        # Генерация ответа через onlysq API
        generated_message = await self.get_onlysq_response(subject)

        if generated_message:
            # Удаление сообщения о генерации
            await asyncio.sleep(1)  # Делаем небольшую задержку для реалистичности
            await generation_message.delete()

            # Отправка финального сообщения с результатом
            await self.client.send_message(
                message.chat_id,
                f"🤖 <b>Я думаю, что {generated_message}!</b>\n\n<i>Разработчик: @xqss_DEVELOPER</i>"
            )

    async def get_onlysq_response(self, subject):
        try:
            # Запрос через onlysq API
            question = f"Какой предмет будет сильнее {subject}, будь они в игре на подобии камень ножницы бумага?....Ответь кратко,без точки,вот так:<предмет> победит {subject}"
            data = [{"role": "user", "content": question}]
            response = requests.post('http://api.onlysq.ru/ai/v1', json=data)
            result = response.json()

            # Получаем ответ
            answer = result.get('answer', '<b>Ответ не получен.</b>')
            return answer
        except Exception as e:
            logger.error(f"Ошибка при запросе к onlysq API: {e}")
            return None
