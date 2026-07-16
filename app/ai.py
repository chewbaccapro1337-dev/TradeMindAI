import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def analyze_trade(image_path: str):

    with open(image_path, "rb") as image:
        image_base64 = base64.b64encode(image.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": ( f"""
                         Ты — профессиональный трейдер ICT / Smart Money Concepts.

                         Проанализируй изображение графика.

                         Ответ верни ТОЛЬКО в таком формате.

                         🧠 TRADEMIND AI
                         ══════════════════════

                         📊 АНАЛИЗ СДЕЛКИ

                         📈 Инструмент
                         Определи инструмент, если его видно. Если нет — напиши "Не определён".

                         ══════════════════════

                         🎯 Направление

                         Укажи:
                         🟢 BUY
                         или
                         🔴 SELL

                         Комментарий:
                         Кратко объясни идею входа.

                         ══════════════════════

                         ⭐ Качество входа

                         Поставь оценку от ★☆☆☆☆ до ★★★★★.

                         После оценки напиши:

                         • качество входа
                         • качество стопа
                         • качество подтверждения
                               
                         ══════════════════════

                         💧 Smart Money

                         Для каждого пункта напиши либо ✅ либо ❌

                         ✅ Liquidity Grab

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ Order Block 

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ Fair Value Gap

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ CHoCH

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ BOS

                         краткое пояснение

                         ══════════════════════

                         ⚖️ Risk / Reward

                         Если видно RR —
                         укажи его.

                         Если нет —
                         напиши "Не удалось определить".

                         После этого дай оценку RR.

                         ══════════════════════

                         ⚠️ Что можно улучшить

                         Напиши 3-5 рекомендаций списком.

                         ══════════════════════

                         🏆 Итоговая оценка

                         Оцени сделку от 0 до 100.

                         Потом поставь рейтинг

                         ⭐⭐☆☆☆
                         или
                         ⭐⭐⭐⭐⭐

                         Вердикт:

                         2-3 предложения с общим выводом.

                         Заканчивай сообщение строкой

                         🤖 TradeMind AI

                         Никаких дополнительных объяснений вне этого шаблона не добавляй.
                         """
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    return response.output_text