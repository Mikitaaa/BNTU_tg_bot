import os
from google import genai

API_KEY = os.environ.get('GEMINI_API_KEY')
PROMPT_MESSAGE = os.environ.get('GEMINI_PROMPT', 'Ответь на вопрос: {user_message}')

if not API_KEY:
    raise ValueError("Переменная окружения GEMINI_API_KEY не установлена")

client = genai.Client(api_key=API_KEY)

def getTextResponse(user_message: str) -> str:
    prompt_message = PROMPT_MESSAGE.format(user_message=user_message)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_message
        )
        return response.text
    except Exception as e:
        print(f"Ошибка при запросе к модели: {e}")
        return "Хз что сказать"
