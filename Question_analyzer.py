import os
from google import genai
from database import get_all_dormitory_data
import time

API_KEY = os.environ.get('GEMINI_API_KEY')
PROMPT_MESSAGE = os.environ.get('GEMINI_PROMPT')
CLASSIFIER_PROMPT = os.environ.get('GEMINI_CLASSIFIER_PROMPT')

if not API_KEY:
    raise ValueError("Переменная окружения GEMINI_API_KEY не установлена")

if not CLASSIFIER_PROMPT:
    raise ValueError("Переменная окружения GEMINI_CLASSIFIER_PROMPT не установлена")

client = genai.Client(api_key=API_KEY)

CATEGORY_DESCRIPTIONS = {
    "room_numbers": "вопросы о комнатах, этажах, размещении, соседях",
    "location": "адрес, как добраться, транспорт",
    "conditions": "условия проживания, удобства, вода, отопление, интернет",
    "dining": "столовая, питание, меню, стоимость еды",
    "sports": "спортзал, тренажеры, площадки",
    "rules": "правила проживания, тишина, комендантский час",
    "payment": "оплата, стоимость, льготы",
    "contacts": "контакты администрации, телефоны, email",
    "faq": "общие вопросы",
    "maintenance": "поломки, ремонт, заявки"
}


def classify_section(user_message: str) -> str:

    descriptions_text = "\n".join(
        f"{key}: {desc}" for key, desc in CATEGORY_DESCRIPTIONS.items()
    )

    prompt = CLASSIFIER_PROMPT.format(
        user_message=user_message,
        categories=", ".join(CATEGORY_DESCRIPTIONS.keys()),
        descriptions=descriptions_text
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        section = response.text.strip().lower()

        if section in CATEGORY_DESCRIPTIONS:
            return section

        return "faq"

    except Exception as e:
        print(f"Ошибка классификации: {e}")
        return "faq"



def get_intelligent_response(user_message: str) -> str:
    relevant_section = classify_section(user_message)
    section_info = get_all_dormitory_data().get(relevant_section, "")
    clean_info = section_info.strip()

    prompt = PROMPT_MESSAGE.format(
        user_message=user_message,
        section_info=clean_info
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:
                print(f"⚠️ Gemini перегружен, попытка {attempt+1}/3")
                time.sleep(1.5 * (attempt + 1))
                continue

            print(f"Ошибка при запросе к модели: {e}")
            return "Извините, не смог обработать ваш вопрос. Попробуйте позже."

    return "Сервис временно недоступен из-за перегрузки. Попробуйте чуть позже."
