import json
from openai import OpenAI
import os


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



def extract_profile(text):


    prompt = f"""

Извлеки информацию о трейдере.

Верни ТОЛЬКО валидный JSON.

Никаких пояснений.
Никакого текста.
Никаких markdown-блоков.
Никаких ```json.

Формат ответа:

{{
  "name": null,
  "trading_style": null,
  "markets": null,
  "timeframes": null,
  "strategies": null,
  "mistakes": null,
  "risk_management": null,
  "goals": null
}}

Сообщение:

{text}

Если информации нет, ставь null.

"""


    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )


    return json.loads(
        response.choices[0].message.content
    )